"""
MapReduce job 

python mr_outputexodus_hadoop.py \
hdfs://icme-hadoop1.localdomain/user/yangyang/simform/predict/p* \
-r hadoop --no-output -o  --variable TEMP \
--outputname = thermal_maze_interpolation
--outdir = hdfs://icme-hadoop1.localdomain/user/yangyang/simform/exodus
--indir = hdfs://icme-hadoop1.localdomain/user/yangyang/simform/

"""

__author__ = 'Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os
from mrjob.job import MRJob

import exopy as ep
from numpy import array, loadtxt
from subprocess import call, check_call, Popen, PIPE, STDOUT

class MROutputExodus(MRJob):

    STREAMING_INTERFACE = MRJob.STREAMING_INTERFACE_TYPED_BYTES
    
    def configure_options(self):
        """Add command-line options specific to this script."""
        super(MROutputExodus, self).configure_options()
        
        self.add_passthrough_option(
            '--variable', dest='variable',
            help='--variable VAR, the variable need to be inserted in the exodus file'       
        )
        self.add_passthrough_option(
            '--outputname', dest='outputname',
            help='--outputname NAME, the name of created new interpolation exodus file'       
        )
        self.add_passthrough_option(
            '--outdir', dest='outdir',
            help='--outdir DIR, Write the output to the directory DIR'       
        )
         self.add_passthrough_option(
            '--indir', dest='indir',
            help='--indir DIR, The HDFS directory you can get the template exodus file '       
        )
    
       
    def load_options(self, args):
        super(MROutputExodus, self).load_options(args)
            
        if self.options.variable is None:
            self.option_parser.error('You must specify the --variable VAR')
        else:
            self.variable = self.options.variable
        
        if self.options.outputname is None:
            self.option_parser.error('You must specify the --outputname NAME')
        else:
            self.outputname = self.options.outputname
            
        if self.options.outdir is None:
            self.option_parser.error('You must specify the --outdir DIR')
        else:
            self.outdir = self.options.outdir
            
        if self.options.indir is None:
            self.option_parser.error('You must specify the --indir DIR')
        else:
            self.indir = self.options.indir
    

    def mapper(self, key, value):     
        """
        input:  (ith new exodus file, time), valarray
        output: ith new exodus file, (time, valarray)
        """
        fnum = key[0]
        time = key[1]
        yield fnum, (time, value)
                
        
    def reducer(self, key, values):
        """
        input: ith new exodus file, (time, valarray, errarray)
        output:ith new exodus file
        """
        
        val_order = {}
        time_order = {}
        
        for i, value in enumerate(values):
            val_order[value[0][0]]=value[1]
            time_order[value[0][0]]=value[0][1]
            
        val = [ ]  
        for k,value in sorted(val_order.iteritems()):
            val.append(value)
        val = array(val)
        
        time = []
        for k,value in sorted(time_order.iteritems()):
            time.append(value)
        time = array(time)
        
        # grab template exodus file from HDFS
        
        tmpstr = self.indir[7:]
        index = tmpstr.find('/')
        prefix = 'hdfs://'+tmpstr[0:index]
        
        cmd = 'hadoop fs -ls '+ dir
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        content = p.stdout.read()
        files = content.split('\n')
        
        flag = True

        for file in files:
            file = file.split(' ')
            fname = file[len(file)-1]
            if fname.endswith('.e'):
                 fname = prefix + fname
            if flag:
                check_call(['hadoop', 'fs', '-copyToLocal', fname, 'template.e'])
                flag = False
        
        template = 'template.e'
        
        # create new interpolation exodus file
        
        if call(['test', '-e', template]) != 0:
            print "The template file doesnot exist!"
            yield key,1
        else:
            print "Reading templatefile %s"%(template)
            templatefile = ep.ExoFile(template,'r')
            
            outfile = self.outputname+str(key)+'.e'
            print "Writing outputfile %s"%(os.path.join(outfile))
            newfile = ep.ExoFile(os.path.join(outfile),'w')  
            
            templatefile.change_nodal_vars2(newfile, time, (self.variable, ), (val,), ('d',))
            
            call(['hadoop', 'fs', '-copyFromLocal', outfile, os.path.join(self.outdir,outfile)])
            newfile.src.sync() 
            newfile.close()
            
            check_call(['rm', '-r', template])
            check_call(['rm', '-r', outfile])
            yield key,0
        
        

if __name__ == '__main__':
    MROutputExodus.run()