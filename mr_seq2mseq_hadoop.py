"""
MapReduce job to compute global variance of a series of simulation runs for all node space.

Example:

python mr_seq2mseq_hadoop.py \
hdfs://icme-hadoop1.localdomain/user/yangyang/simform/output2/data/thermal_maze00*/thermal_*.seq \
-r hadoop --no-output -o tsqr/exodus.bseq --variable TEMP 

"""

__author__ = 'Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os

from mrjob.job import MRJob
from numpy import *

class MRSeq2Mseq(MRJob):

    STREAMING_INTERFACE = MRJob.STREAMING_INTERFACE_TYPED_BYTES
    
    def configure_options(self):
        """Add command-line options specific to this script."""
        super(MRSeq2Mseq, self).configure_options()
        
        self.add_passthrough_option(
            '--variable', dest='variable',
            help='--variable VAR, the variable need to compute global variance'       
        )
       
    def load_options(self, args):
        super(MRSeq2Mseq, self).load_options(args)
            
        if self.options.variable is None:
            self.option_parser.error('You must specify the --variable VAR')
        else:
            self.variable = self.options.variable
    
    def mapper(self, key, value):
        """
        output: (timestep,node), (param,value)
        """
        # ignore coordinate (x,y,z) data
        if (key != -1) and (key != -2) and (key != -3) : 
            for i, var in enumerate(value):
                name = var[0]
                if name == self.variable:
                    p = int(key[0])
                    t = key[1]
                    for j, val in enumerate(var[1]):
                        yield (t,j), (p,val)
     

    def reducer(self, key, values): 
        """ 
        Each key is a (timestep, node) pair.  Each value is (param,value) pair.
        We want to make an array of all the values over the parameters. 
        """
        valarray = [val for val in values] # realize the 
        array = [0. for _ in xrange(len(valarray))]
        for val in valarray:
            pi = val[0]
            v = val[1]
            array[pi-1] = v
            
        yield key, array  
        
    def steps(self):
        return [self.mr(self.mapper, self.reducer),]

if __name__ == '__main__':
    MRSeq2Mseq.run()

