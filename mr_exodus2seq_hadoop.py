"""
MapReduce job to convert a set of raw exodus files to corresponding sequence files.
The mapper just reads the file name, fetches the file and converts it into a set of 
sequence files.

History
-------
:2012-06-22: avoid PICKLE type code
:2012-08-09: fix the bugs if tasks fail 

Example(on ICME Hadoop):

python mr_exodus2seq_hadoop.py hdfs://icme-hadoop1.localdomain/user/yangyang/simform/input.txt \
-r hadoop -t 10 -d hdfs://icme-hadoop1.localdomain/user/yangyang/simform/output3/data --variables TEMP \
--timestepfile timesteps.txt  --python-archive simform-deploy.tar.gz --file timesteps.txt

"""

__author__ = 'Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os
from subprocess import call, check_call

from mrjob.compat import get_jobconf_value
from mrjob.job import MRJob

import exopy2 as ep

from hadoop.io import SequenceFile
from hadoop.io.SequenceFile import CompressionType
from hadoop.typedbytes import *

def linear_interpolate(x,x1,y1,x2,y2):
    slope = (y2 - y1)/(x2 - x1)
    y = (x - x1)*slope + y1
    return y
    
def convert(inputfile, steps, outdir, variables, normalized_timesteps):
    fset = 0
    
    fdir,fname = os.path.split(inputfile)
    fsetnum=''
    for i,c in enumerate(fname):
        if c.isdigit():
            fsetnum+=c
    fset=int(fsetnum)
        
    f = ep.ExoFile(inputfile,'r')
        
    Vars = variables.split(',')
    
    # Get time data and coordinate (x,y,z) data
    time = f.cdf.variables["time_whole"]
    timedata = time.getValue()
    coordz = f.cdf.variables["coordz"]
    zdata = coordz.getValue()
    coordy = f.cdf.variables["coordy"]
    ydata = coordy.getValue()
    coordx = f.cdf.variables["coordx"]
    xdata = coordx.getValue()
    
    # To avoid PICKLE type in typedbytes files
    timedata2 = []
    for i, ele in enumerate(timedata):
        timedata2.append(float(ele))
    xdata2 = []
    for i, ele in enumerate(xdata):
        xdata2.append(float(ele))
    ydata2 = []
    for i, ele in enumerate(ydata):
        ydata2.append(float(ele))
    zdata2 = []
    for i, ele in enumerate(zdata):
        zdata2.append(float(ele))
    
    # Note: the size of normalized_timesteps should not be greater than 
    # num_time_steps in the exodus file.
    if normalized_timesteps is None:
        normalized_timesteps = timedata2
    
    total_time_steps = len(normalized_timesteps)
    
    # Get variable data
    varnames = f.node_variable_names()
    vardata = []
    for i, var in enumerate(Vars):
        vdata = None
        for vi,n in enumerate(varnames):
            if n == var.strip():
                #vtemp = vi
                vindex = vi
                break
        if vindex == None:
            print  >> sys.stderr, 'The variable ', var.strip(), 'does not exist!'
            return False
        tmp = f.vars['vals_nod_var'+str(vindex+1)]
        tmpdata = tmp.getValue()
        vardata.append((var.strip(), tmpdata))
    
    # Begin to partition
    basename = os.path.basename(inputfile)
    ind = basename.rfind('.')
    basename = basename[0:ind]
    
    indexkey = TypedBytesWritable()
    indexvalue = TypedBytesWritable()
    indexwriter = SequenceFile.createWriter(os.path.join(outdir,'index.seq'), 
        TypedBytesWritable, TypedBytesWritable,compression_type=CompressionType.RECORD)
    
    begin = 0
    i = 0
    
    time_begin = 0
    
    while begin < total_time_steps:
        end = begin + steps - 1
        if end > total_time_steps - 1:
            end = total_time_steps - 1
        outputfilename = basename + '_part'+ str(i) + '.seq'
        
        writer = SequenceFile.createWriter(os.path.join(outdir,outputfilename),
            TypedBytesWritable, TypedBytesWritable,compression_type=CompressionType.RECORD)
        key = TypedBytesWritable()
        value = TypedBytesWritable()
        key.set(-1)
        value.set(xdata2)
        writer.append(key,value)
        key.set(-2)
        value.set(ydata2)
        writer.append(key,value)
        key.set(-3)
        value.set(zdata2)
        writer.append(key,value)
        
        for j in xrange(begin, end+1):
            key.set((fset,(j,normalized_timesteps[j])))
            valuedata = []
            for m, var in enumerate(vardata):
                name = var[0]
                data = var[1]
                for t in xrange(time_begin, len(timedata2)):
                    if normalized_timesteps[j] == timedata2[t]:
                        normalized_data = data[t]
                        time_begin = t
                        break
                    elif normalized_timesteps[j] < timedata2[t]:
                        normalized_data =  linear_interpolate(normalized_timesteps[j], timedata2[t-1], data[t-1], timedata2[t], data[t])
                        break
                data2 = []
                for m, ele in enumerate(normalized_data):
                    data2.append(float(ele))
                valuedata.append((name,data2))
            value.set(valuedata)
            writer.append(key,value)
        writer.close()
        indexkey.set(outputfilename)
        indexvalue.set(end-begin+1)
        indexwriter.append(indexkey,indexvalue)
        begin = begin + steps
        i = i + 1
        
    indexkey.set('total')
    indexvalue.set(total_time_steps)
    indexwriter.append(indexkey,indexvalue)   
    indexwriter.close()
    
    return True
    
    
    
class MRExodus2Seq(MRJob):

    MRJob.HADOOP_INPUT_FORMAT = 'org.apache.hadoop.mapred.lib.NLineInputFormat'
    
    def configure_options(self):
        """Add command-line options specific to this script."""
        super(MRExodus2Seq, self).configure_options()
        
        self.add_passthrough_option(
            '-t', '--timesteps', dest='timesteps',
            type='int',
            help='-t NUM or --timesteps NUM, Groups the output into batches of NUM timesteps'       
        )
        self.add_passthrough_option(
            '-d', '--outdir', dest='outdir',
            help='-d DIR or --outdir DIR, Write the output to the directory DIR'
        )
        self.add_passthrough_option(
            '--variables', dest='variables',
            help='--variables VARS, Only output the variables in the comma delimited list'       
        )
        self.add_passthrough_option(
            '--timestepfile', dest='timestepfile',
            help='--timestepfile FILE, Get the normalized timesteps'       
        )
       
    def load_options(self, args):
        super(MRExodus2Seq, self).load_options(args)
        
        if self.options.timesteps is None:
            self.option_parser.error('You must specify the --timesteps NUM or -t NUM')
        else:
            self.timesteps = self.options.timesteps
            
        if self.options.outdir is None:
            self.option_parser.error('You must specify the --outdir DIR or -d DIR')
        else:
            self.outdir = self.options.outdir
            
        if self.options.variables is None:
            self.option_parser.error('You must specify the --variables VARS')
        else:
            self.variables = self.options.variables
       
        if self.options.timestepfile is None:
            self.timestepfile = None
        else:
            self.timestepfile = self.options.timestepfile
            
    
    def mapper(self, _, line):
        # step 0: strip off unexpected characters
        line = line.split('\t')[1]
        
        # step 1: fetch the exodus file from Hadoop cluster
        file = os.path.basename(line)
        if os.path.isfile(os.path.join('./', file)):
            call(['rm', os.path.join('./', file)])
        check_call(['hadoop', 'fs', '-copyToLocal', line, os.path.join('./', file)])
        outdir = os.path.basename(line)
        ind = outdir.rfind('.')
        outdir = outdir[0:ind]
        if os.path.isdir(os.path.join('./', outdir)):
            call(['rm', '-r', os.path.join('./', outdir)])
        call(['mkdir', os.path.join('./', outdir)])
        
        # step 2: do our local processing
        if self.timestepfile is None:
            lines = None
        else:
            f = open(os.path.basename(self.timestepfile))
            lines = f.readlines()
            for i in xrange(0, len(lines)):
                lines[i]=float(lines[i].strip())
            
        result = convert(os.path.join('./', file), self.timesteps, os.path.join('./', outdir), self.variables,lines)
        
        # step3: write back to Hadoop cluster
        user = get_jobconf_value('mapreduce.job.user.name')
       
        for fname in os.listdir(os.path.join('./', outdir)):
            if call(['hadoop', 'fs', '-test', '-e', os.path.join(self.outdir,outdir,fname)]) == 0:
                call(['hadoop', 'fs', '-rm', os.path.join(self.outdir,outdir,fname)])
            call(['hadoop', 'fs', '-copyFromLocal', os.path.join('./',outdir,fname),os.path.join(self.outdir,outdir,fname)])
            call(['hadoop', 'fs', '-chown', '-R', user, os.path.join(self.outdir)])
        call(['rm', os.path.join('./', file)])
        call(['rm', '-r', os.path.join('./', outdir)])
        
        #step 4: yield output key/value
        if result == True:
            yield (line, 0)
        else:
            yield (line, 1)
        
    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRExodus2Seq.run()
