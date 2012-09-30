"""
Check and compare the timestamps of two URI on the HDFS  

Example:
python check_time.py left_path right_path

"""

__author__ = 'Yangyang Hou <hyy.sun@gmail.com>'

import os
import sys
import time
from subprocess import Popen, PIPE, STDOUT


def getstat(path):
    """ Get the timestamps of the URI on the HDFS """
    cmd = 'hadoop fs -stat '+path
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    content = p.stdout.read()
    timestrs = content.split('\n')
    timestrs = timestrs[:len(timestrs)-1]
    times = []
    for str in timestrs:
        tmp = time.strptime(str,"%Y-%m-%d %H:%M:%S")
        times.append(tmp)
        
    return times
    

def checktime(left_path, right_path):
    """
    Check and compare the timestamps of two URI on the HDFS
    If one in left_path is newer than one in right_path, return True
    Otherwise, return False
    """
    left_times = getstat(left_path)
    right_times = getstat(right_path)
    for left_time in left_times:
        for right_time in right_times:
            if left_time > right_time:
                return True
    
    return False


if __name__ == '__main__':
    left_path = sys.argv[1]
    right_path = sys.argv[2]
    result = checktime(left_path, right_path)
    if result:
        sys.exit(0)
    else:
        sys.exit(1)
    
