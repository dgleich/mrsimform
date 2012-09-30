__author__ = 'Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os
from subprocess import call, check_call, Popen, PIPE, STDOUT
from check_time import checktime

dir = sys.argv[1]
tmpdir = sys.argv[2]

tmpstr = dir[7:]
index = tmpstr.find('/')
prefix = 'hdfs://'+tmpstr[0:index]

cmd = 'hadoop fs -ls '+ dir
p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
content = p.stdout.read()
files = content.split('\n')

print "Automatically grab template file from HDFS..."
flag = True

for file in files:
    file = file.split(' ')
    fname = file[len(file)-1]
    if fname.endswith('.e'):
        fname = prefix + fname
        if flag:
            call(['mkdir', os.path.join(tmpdir, 'tmp')])
            
            check_call(['hadoop', 'fs', '-copyToLocal', fname, os.path.join(tmpdir, 'tmp/template.e')])
            flag = False
            
print "Done!"
