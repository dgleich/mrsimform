"""
MapReduce job 

python mr_predict_hadoop.py \
hdfs://icme-hadoop1.localdomain/user/yangyang/simform/output3/data/thermal_maze00*/thermal_*.seq \
-r hadoop --no-output -o new_points --variable TEMP \
--design=design_points.txt --points=new_points.txt \
--file design_points.txt --file new_points.txt 
"""

__author__ = 'Paul ''Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os
from mrjob.job import MRJob

from numpy import zeros,exp,linspace,dot,sum,mgrid,loadtxt
from numpy.linalg import cholesky,solve,norm
from numpy import *



def grbf_weights(S=None, X=None, rho=1.0):
    """
    Weights for computing the Gaussian radial basis interpolant on
    a set of points.
    Inputs:
    rho  Gaussian RBF parameter
    S    Design sites, array of size ns-by-d, where d is dimension
         and ns is the number of design sites.
    X    Interpolation sites, array of size nx-by-d, where nx is
         the number of interpolation sites.
    Outputs:
         Set of interpolation weights, array of size ns-by-nx.
    """
    rho=rho*rho
    C=exp(-rho*distances_sq(S,S))
    L=cholesky(C)
    D=exp(-rho*distances_sq(S,X))
    return solve(L.T,solve(L,D))

def distances_sq(S1=None,S2=None):
    """ Compute the squared distances between sets of points"""
    n1=S1.shape[0]
    n2=S2.shape[0]
    D=zeros((n1,n2))
    if S1.ndim==1:
        for i in range(n1):
            for j in range(n2):
                D[i,j]=(S1[i]-S2[j])**2
    else:
        for i in range(n1):
            for j in range(n2):
                D[i,j]=sum((S1[i,:]-S2[j,:])**2)
    return D


class MRPredict(MRJob):

    STREAMING_INTERFACE = MRJob.STREAMING_INTERFACE_TYPED_BYTES
    
    def configure_options(self):
        """Add command-line options specific to this script."""
        super(MRPredict, self).configure_options()
        
        self.add_passthrough_option(
            '--variable', dest='variable',
            help='--variable VAR, the variable need to compute global variance'       
        )
        self.add_passthrough_option(
            '--design', dest='design',
            help='--design FILE, design sites'       
        )
        self.add_passthrough_option(
            '--points', dest='points',
            help='--points FILE, Interpolation sites'       
        )
       
    def load_options(self, args):
        super(MRPredict, self).load_options(args)
            
        if self.options.variable is None:
            self.option_parser.error('You must specify the --variable VAR')
        else:
            self.variable = self.options.variable
            
        if self.options.design is None:
            self.option_parser.error('You must specify the --design FILE')
        else:
            self.design = self.options.design
            
        if self.options.points is None:
            self.option_parser.error('You must specify the --points FILE')
        else:
            self.points = self.options.points
    

    def mapper(self, key, value):     
        design_points = loadtxt(os.path.basename(self.design))
        new_points = loadtxt(os.path.basename(self.points))
        W=grbf_weights(design_points,new_points) # interpolation weights
        
        if (key != -1) and (key != -2) and (key != -3) : 
            p=key[0]
            t=key[1]
            for i, var in enumerate(value):
                name = var[0]
                if name == self.variable:
                    val = var[1]
                    val = array(val)
                    n = val.size
                    for j in range(len(new_points)):
                        weighted_value = W.T[j,p-1]*val
                        yield (j,t,n), weighted_value
        
    def reducer(self, key, values):
        data = zeros(key[2])
        for i, var in enumerate(values):
            data = data + var
        yield (key[0],key[1]), data
        

if __name__ == '__main__':
    MRPredict.run()