"""
MapReduce job 

python mr_predictwithSVD_hadoop.py \
hdfs://icme-hadoop1.localdomain/user/yangyang/simform/output/model_4/p* \
-r hadoop --no-output -o predict --weights=weights.txt --file weights.txt 
"""

__author__ = 'Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os
from mrjob.job import MRJob

from numpy import array, loadtxt

class MRPredictwithSVD(MRJob):

    STREAMING_INTERFACE = MRJob.STREAMING_INTERFACE_TYPED_BYTES
    
    def configure_options(self):
        """Add command-line options specific to this script."""
        super(MRPredictwithSVD, self).configure_options()
        
        self.add_passthrough_option(
            '--weights', dest='weights',
            help='--weights FILE, the file of interpolation weights with SVD'       
        )
    
       
    def load_options(self, args):
        super(MRPredictwithSVD, self).load_options(args)
            
        if self.options.weights is None:
            self.option_parser.error('You must specify the --weights FILE')
        else:
            self.weights = self.options.weights
    

    def mapper(self, key, value):     
        """
        input:  (timestep,node), value
        output: (ith new exodus file,time),(node, val, err)
        """
       
        W=loadtxt(os.path.basename(self.weights)) # interpolation weights
        
        time = key[0]
        node = key[1]
        for i, weight in enumerate(W):
            K = weight[0] # number of left singular vectors to compute the interpolation
            val = 0
            err = 0
            for j in range(K):
                val += value[j]*weight[j+1]
            for j in range (K,len(value)):
                err += (value[j]*weight[j+1])*(value[j]*weight[j+1])
            
            yield (i,time), (node, val, err)
                
        
    def reducer(self, key, values):
        """
        input: (ith new exodus file, time), (node, val, err)
        output:(ith new exodus file, time), (valarray, errarray)
        """
        
        val_order = {}
        err_order = {}
        
        for i, value in enumerate(values):
            val_order[value[0]]=value[1]
            err_order[value[0]]=value[2]
            
        val = [ ]  
        for k,value in sorted(val_order.iteritems()):
            val.append(value)
        val = array(val)
        
        err = [ ]  
        for k,value in sorted(err_order.iteritems()):
            err.append(value)
        err = array(err)
        
        yield key, (val, err)

if __name__ == '__main__':
    MRPredictwithSVD.run()