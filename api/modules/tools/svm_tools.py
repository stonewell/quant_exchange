import sys
import os
from subprocess import *
from threading import Thread

if(sys.hexversion < 0x03000000):
	import Queue
else:
	import queue as Queue

#global parameters
fold = 5
c_begin, c_end, c_step = -5,  15, 2
g_begin, g_end, g_step =  3, -15, -2
nr_local_worker = 1

class WorkerStopToken:  # used to notify the worker to stop
        pass

class Worker(Thread):
    def __init__(self,name,job_queue,result_queue, svmtrain_exe, dataset_pathname):
        Thread.__init__(self)
        self.name = name
        self.job_queue = job_queue
        self.result_queue = result_queue
        self.svmtrain_exe = svmtrain_exe
        self.dataset_pathname = dataset_pathname
        
    def run(self):
        while True:
            (cexp,gexp) = self.job_queue.get()
            if cexp is WorkerStopToken:
                self.job_queue.put((cexp,gexp))
                # print('worker {0} stop.'.format(self.name))
                break
            try:
                rate = self.run_one(2.0**cexp,2.0**gexp)
                if rate is None: raise RuntimeError("get no rate")
            except:
                # we failed, let others do that and we just quit
                self.job_queue.put((cexp,gexp))
                print('worker {0} quit.'.format(self.name))
                break
            else:
                self.result_queue.put((self.name,cexp,gexp,rate))

class LocalWorker(Worker):
    def run_one(self,c,g):
        cmdline = '{0} -c {1} -g {2} -v {3} {4} {5}'.format \
          (self.svmtrain_exe,c,g,fold, ' ' , self.dataset_pathname)
        result = Popen(cmdline,shell=True,stdout=PIPE).stdout
        for line in result.readlines():
            if str(line).find("Cross") != -1:
                return float(line.split()[-1][0:-1])

def calculate_jobs():
    c_seq = permute_sequence(range_f(c_begin,c_end,c_step))
    g_seq = permute_sequence(range_f(g_begin,g_end,g_step))
    nr_c = float(len(c_seq))
    nr_g = float(len(g_seq))
    i = 0
    j = 0
    jobs = []

    while i < nr_c or j < nr_g:
        if i/nr_c < j/nr_g:
            # increase C resolution
            line = []
            for k in range(0,j):
                line.append((c_seq[i],g_seq[k]))
            i = i + 1
            jobs.append(line)
        else:
            # increase g resolution
            line = []
            for k in range(0,i):
                line.append((c_seq[k],g_seq[j]))
            j = j + 1
            jobs.append(line)
    return jobs

def range_f(begin,end,step):
    # like range, but works on non-integer too
    seq = []
    while True:
        if step > 0 and begin > end: break
        if step < 0 and begin < end: break
        seq.append(begin)
        begin = begin + step
    return seq

def permute_sequence(seq):
    n = len(seq)
    if n <= 1: return seq

    mid = int(n/2)
    left = permute_sequence(seq[:mid])
    right = permute_sequence(seq[mid+1:])

    ret = [seq[mid]]
    while left or right:
        if left: ret.append(left.pop(0))
        if right: ret.append(right.pop(0))

    return ret

class SvmTools(object):
    def __init__(self, svm_bin_path):
        # svm, grid, and gnuplot executable files
        is_win32 = (sys.platform == 'win32')

        if is_win32:
            self.svmscale_exe = os.path.join(svm_bin_path, "svm-scale.exe")
            self.svmtrain_exe = os.path.join(svm_bin_path, "svm-train.exe")
            self.svmpredict_exe = os.path.join(svm_bin_path,"svm-predict.exe")
        else:
            self.svmscale_exe = os.path.join(svm_bin_path, "svm-scale")
            self.svmtrain_exe = os.path.join(svm_bin_path, "svm-train")
            self.svmpredict_exe = os.path.join(svm_bin_path,"svm-predict")

        assert os.path.exists(self.svmscale_exe),"svm-scale executable not found:%s" % self.svmscale_exe
        assert os.path.exists(self.svmtrain_exe),"svm-train executable not found:%s" % self.svmtrain_exe
        assert os.path.exists(self.svmpredict_exe),"svm-predict executable not found:%s" % self.svmpredict_exe

    def gen_model(self, train_pathname, model_file, range_file, tmp_path, lower_limit = -1):
        assert os.path.exists(train_pathname),"training file not found"
        file_name = os.path.split(train_pathname)[1]
        scaled_file = os.path.join(tmp_path, file_name + ".scale")

        cmd = '{0} -l {4} -s "{1}" "{2}" > "{3}"'.format(self.svmscale_exe, range_file, train_pathname, scaled_file, lower_limit)
        print('Scaling training data...')
        Popen(cmd, shell = True, stdout = PIPE).communicate()	

        print('Cross Validation data...')
        c,g,rate = self.cross_validation_model(scaled_file)

        print('Best c={0}, g={1} CV rate={2}'.format(c,g,rate))

        cmd = '{0} -c {1} -g {2} "{3}" "{4}"'.format(self.svmtrain_exe,c,g,scaled_file,model_file)
        print('Training...')
        Popen(cmd, shell = True, stdout = PIPE).communicate()

        print('Output model: {0}'.format(model_file))

    def cross_validation_model(self, scale_file):
        # put jobs in queue

        jobs = calculate_jobs()
        job_queue = Queue.Queue(0)
        result_queue = Queue.Queue(0)

        for line in jobs:
            for (c,g) in line:
                job_queue.put((c,g))

        # hack the queue to become a stack --
        # this is important when some thread
        # failed and re-put a job. It we still
        # use FIFO, the job will be put
        # into the end of the queue, and the graph
        # will only be updated in the end
        job_queue._put = job_queue.queue.appendleft
        
        # fire local workers
        for i in range(nr_local_worker):
            LocalWorker('local',job_queue,result_queue, self.svmtrain_exe, scale_file).start()

        # gather results
        done_jobs = {}

        best_rate = -1
        best_c1,best_g1 = None,None

        for line in jobs:
            for (c,g) in line:
                while (c, g) not in done_jobs:
                    (worker,c1,g1,rate) = result_queue.get()
                    done_jobs[(c1,g1)] = rate

                    if (rate > best_rate) or (rate==best_rate and g1==best_g1 and c1<best_c1):
                        best_rate = rate
                        best_c1,best_g1=c1,g1
                        best_c = 2.0**c1
                        best_g = 2.0**g1
                #end while
            #end for (c,g)
        #end for line

        job_queue.put((WorkerStopToken,None))
        return (best_c, best_g, best_rate)
        
    def gen_predict(self, predict_data_file_name, model_file, range_file, tmp_path, lower_limit = -1):
        file_name = os.path.split(predict_data_file_name)[1]
        scaled_test_file = os.path.join(tmp_path, file_name + ".scale")
        predict_test_file = os.path.join(tmp_path, file_name + ".predict_test")
        
        cmd = '{0} -l {4} -r "{1}" "{2}" > "{3}"'.format(self.svmscale_exe, range_file, predict_data_file_name,
                                                  scaled_test_file, lower_limit)
        print('Scaling testing data...')
        Popen(cmd, shell = True, stdout = PIPE).communicate()	

        cmd = '{0} "{1}" "{2}" "{3}" && cat "{3}"'.format(self.svmpredict_exe, scaled_test_file, model_file, predict_test_file)
        print('Testing...')

        result = Popen(cmd, shell = True, stdout= PIPE).stdout

        level = 0

        for line in result.readlines():
            try:
                print(line)
                level = int(line)
            except:
                pass
        return level

