# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
from traceback import print_exception

def k_means(data, cluster_count):
    assert cluster_count >= 2, "cluster count must exceed 2"
    assert len(data) >= cluster_count, "too few data for " + str(cluster_count) + " cluster(s)"

    data.sort()
    
    #generate center
    center = []

    for i in range(0, cluster_count):
        pos = int(len(data) * i / cluster_count)
        center.append(data[pos])

    data_cluster = {} #data belongs to which cluster
    cluster_count_dict = {} #data count belongs to cluster
    cluster_sum_dict = {} #sum for cluster members

    cluster_changed = False
    first_run = True
    
    while first_run or cluster_changed:
        cluster_changed = False

        cluster_count_dict = {}
        cluster_sum_dict = {}

        for v in data:
            start = 0

            while start < len(center) and center[start] == -1:
                start += 1

            assert start != len(center), "unable to figure out cluster"
                
            min = abs(v - center[start])
            cluster = start

            for i in range(start + 1, cluster_count):
                if (center[i] == -1):
                    continue
                
                delta = abs(v - center[i])
                if min > delta:
                    min = delta
                    cluster = i
            #end for

            if not first_run and not cluster_changed:
                cluster_changed = data_cluster[v] != cluster
            #end if

            data_cluster[v] = cluster

            if cluster_count_dict.has_key(cluster):
                cluster_count_dict[cluster] = cluster_count_dict[cluster] + 1
            else:
                cluster_count_dict[cluster] = 1

            if cluster_sum_dict.has_key(cluster):
                cluster_sum_dict[cluster] = cluster_sum_dict[cluster] + v
            else:
                cluster_sum_dict[cluster] = v
        #end for

        #update center
        for cluster in range(0, cluster_count):
            if cluster_sum_dict.has_key(cluster):
                center[cluster] = cluster_sum_dict[cluster] / cluster_count_dict[cluster]
            else:
                center[cluster] = -1

        first_run = False
    #end while

    return {center[cluster] : cluster_count_dict[cluster] for cluster in cluster_count_dict.keys()}
#end def

if __name__ == '__main__':
    try:
        assert os.path.isfile(sys.argv[1]), "must provide data file"

        f = open(sys.argv[1])
        
        data = [float(line) for line in f.readlines()]

        print(k_means(data, 8))
    except:
        type, value, traceback = sys.exc_info()
        print("Unpected Error:", value)
        print_exception(type, value, traceback)
