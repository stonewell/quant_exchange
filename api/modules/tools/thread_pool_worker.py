from __future__ import print_function

import sys
import os
import logging
from threading import Thread

if(sys.hexversion < 0x03000000):
	import Queue
else:
	import queue as Queue

from time import sleep

class WorkerStopToken:  # used to notify the worker to stop
        pass

class Task:
    def __init__(self, name):
        self.name = name
        self.done = False
        self.failed = False
        
    def run_one(self):
        pass

    def done(self):
        return self.done

    def failed(self):
        return self.failed
    
class Worker(Thread):
    def __init__(self,name, job_queue):
        Thread.__init__(self)
        self.name = name
        self.daemon = True
        self.job_queue = job_queue
        logging.debug('worker {0} created.'.format(self.name))
        
    def run(self):
        while True:
            task = self.job_queue.get()
            if isinstance(task, WorkerStopToken) or not hasattr(task, 'run_one') or task is None:
                if task is not None:
	                self.job_queue.put(task)
                logging.debug('worker {0} stop.'.format(self.name))
                break
            try:
                logging.debug('worker {0} started task.'.format(self.name))
                task.run_one()
                logging.debug('worker {0} finished task.'.format(self.name))
            except:
                # we failed, let others do that and we just quit
                if hasattr(task, 'name'):
                    logging.exception('worker {0} run task {1} fail.'.format(self.name, task.name))
                else:
                    logging.exception('worker {0} run task fail.'.format(self.name))
        #end while
    #end def run

class ThreadPoolWorker:
    def __init__(self, _worker_count = 5):
        self.worker_count = _worker_count
        self.job_queue = self.__get_queue()

    def add_task(self, task):
        self.job_queue.put(task)

    def shutdown(self):
        self.job_queue.put(WorkerStopToken())
        
    def start(self):
        # fire local workers
        for i in range(self.worker_count):
            Worker('local_{0}'.format(i), self.job_queue).start()

    def job_queue(self):
        return self.job_queue

    def __get_queue(self):
        return Queue.Queue(0)
        
def wait_all_task_done(tasks, timeout=10):
    all_done = False
    
    while not all_done:
        all_done = True
        
        for task in tasks:
            if not task.done and not task.failed:
                all_done = False
                break
            
        if not all_done:
            sleep(timeout) #sleep for 10
#end wait_all_task_done            

def wait_for_all_pids(pids):
    for pid in pids:
        try:
            os.waitpid(pid, 0)
        except:
            logging.exception('wait for child process:{0} fail'.format(pid))
#end def wait_for_all_pids            

def wait_for_any_child():
    try:
        pid, status = os.wait()
        return pid
    except:
        logging.exception('wait for any child fail')
        return 0
#end def wait_for_any_child
