#! /usr/bin/env python
from numpy import *

try:
    import Scientific.IO.NetCDF as netcdf
except ImportError:
    import pynetcdf as netcdf
#import pupynere as netcdf
#import scipy.io.netcdf as netcdf


import re
import types
import pdb
import os, sys, math, random, time
import os.path
import glob

class ExoFile:
	# NOTE seem to be some issues with variable assignments, should use the assignValue()
	#      netCDF statement to assign values to numpy arrays
	def __init__(self,filename, a):
		"""
		filename is a string containing the file name,
		a is a character:  r - read only, w - read write, a - open existing or create new
		"""
		self.src = netcdf.NetCDFFile(filename, a)
		self.dimensions = self.src.dimensions
		self.variables = self.src.variables

	def close(self):
		"""
		Closes file after changes have occurred
		"""
		self.src.close()

	def num_nodes(self,*args):   
		"""
		Get/Set method for the number of nodes.
		If no args are passed, then it returns number of nodes.
		If an arg is passed it will set the number of nodes to the number passed. 
		"""
		if len(args) == 0:
			return self.src.dimensions["num_nodes"]
		elif len(args) == 1:
			self.src.dimensions["num_nodes"] = args[0]

	def num_dim(self,*args):
		"""
		Get/Set method for the number of physical dimensions.
		If no args are passed, then it returns number of dims.
		If an arg is passed it will set the number of dims to the number passed. 
		"""
		if len(args) == 0:
			return self.src.dimensions["num_dim"]
		if len(args) == 1:
			self.src.dimensions["num_dim"] = args[0]

	def num_elem(self,*args):
		"""
		Get/Set Method for the Number of Elements in the exodus file
		If no args are passed, then it returns number of elems.
		If an arg is passed it will set the number of elems to the number passed.
		"""
		if len(args) == 0:
			return self.src.dimensions["num_elem"]
		if len(args) == 1:
			self.src.dimensions["num_elem"] = args[0]

	def num_el_blk(self,*args):
		"""
		Get/Set Method for the Number of blocks in the exodus file
		If no args are passed, then it returns number of blocks.
		If an arg is passed it will set the number of blocks to the number passed.
		"""
		if len(args) == 0:
			return self.src.dimensions["num_el_blk"]
		if len(args) == 1:
			self.src.dimensions["num_el_blk"] = args[0]

	def num_side_sets(self,*args):
		"""
		Get/Set method for the number of side sets.
		If no args are passed, then it returns number of side sets.
		If an arg is passed it will set the number of sidesets to the number passed.
		"""
		if len(args) == 0:
			return self.src.dimensions["num_side_sets"]
		if len(args) == 1:
			self.src.dimensions["num_side_sets"] = args[0]

	def num_node_sets(self,*args):
		"""
		Get/Set method for the number of node sets.
		If no args are passed, then it returns number of node sets.
		If an arg is passed it will set the number of nodesets to the number passed.
		"""
		if len(args) == 0:
			return self.src.dimensions["num_node_sets"]
		if len(args) == 1:
			self.src.dimensions["num_node_sets"] = args[0]
        
	def num_qa_rec(self,*args):
		"""
		Get/Set method for the number of QA records.
		If no args are passed, then it returns number of QA records.
		If an arg is passed it will set the number of QA records to the number passed.
		"""
		if len(args) == 0:
			return self.src.dimensions["num_qa_rec"]
		if len(args) == 1:
			self.src.dimensions["num_qa_rec"] = args[0]

	def num_info(self,*args):
		"""
		Get/Set method for the number of information records.
		If no args are passed, then it returns number of information records.
		If an arg is passed it will set the number of dims to the number passed. 
		"""
		if len(args) == 0:
			return self.src.dimensions["num_info"]
		if len(args) == 1:
			self.src.dimensions["num_info"] = args[0]

	def num_el_in_blk(self,eb_num):
		"""
		Get method for the number of elements in a block.
		Only argument is the block id
		"""
		eb_num_st = repr(eb_num)
		num_el_in_blk = "num_el_in_blk"+eb_num_st
		return self.src.dimensions[num_el_in_blk]

	def num_glo_var(self,*args):
		"""
		Get/Set method for the number of global variables
		If no args are passed, then it returns number of global variables.
		If an arg is passed it will set the number of global variables to the number passed. 
		"""
		if len(args) == 0:
			return self.src.dimensions["num_glo_var"]
		if len(args) == 1:
			self.src.dimensions["num_glo_var"] = args[0]

	def num_nod_var(self,*args):
		"""
		Get/Set method for the number of nodal variables.
		If no args are passed, then it returns number of nodal variables
		If an arg is passed it will set the number of nodal variables to the number passed. 
		"""
		if len(args) == 0:
			return self.src.dimensions["num_nod_var"]
		if len(args) == 1:
			self.src.dimensions["num_nod_var"] = args[0]
                    
	def num_elem_var(self,*args):
		"""
		Get/Set method for the number of elemental variables.
		If no args are passed, then it returns number of elemental variables.
		If an arg is passed it will set the number of elemental variable to the number passed. 
		"""
		if len(args) == 0:
			return self.src.dimensions["num_elem_var"]
		if len(args) == 1:
			self.src.dimensions["num_elem_var"] = args[0]

	def num_time_steps(self):
		"""
		Gets number of time steps
		"""
		time_whole = self.src.variables["time_whole"].getValue()
		return len(time_whole)

	def time_step(self,index):
		"""
		Gets the time value of a certain index
		Only argument is index id
		"""
		time_whole = self.src.variables["time_whole"].getValue()
		return time_whole[index]

	def len_string(self,*args):
		"""
		Get/Set method for the string length in number of characters.
		If no args are passed, then it returns string length.
		If an arg is passed it will set the string length to the number passed.
		"""
		if len(args) == 0:
			return self.src.dimensions["len_string"]
		if len(args) == 1:
			self.src.dimensions["len_string"] = args[0]

	def len_line(self,*args):
		"""
		Get/Set method for the line length in number of characters.
		If no args are passed, then it returns line length.
		If an arg is passed it will set the line length to the number passed.  
		"""
		if len(args) == 0:
			return self.src.dimensions["len_line"]
		if len(args) == 1:
			self.src.dimensions["len_line"] = args[0]

	def num_nod_per_el(self,*args):
		"""
		Get/Set method for the number of nodes in a given element block.
		If one arg are passed, then it returns number of nodes in a given element block.
		If two args is passed it will set the number of nodes in a given element block. 
		"""
		name = "num_nod_per_el" + repr(args[0])
		if len(args) == 1:
			return self.src.dimensions[name]          
		if len(args) == 2:
			self.src.dimensions[name] = args[1]

	def num_el_in_blk(self,*args):
		"""
		Get/Set method for the number of elements in a given element block
		If one arg is passed, then it returns elements in a given element block
		If two args is passed it will set the number of elements in a given element block to the number passed. 
		"""
		name = "num_el_in_blk" + repr(args[0])
		if len(args) == 1:
			return self.src.dimensions[name]
		if len(args) == 2:
			self.src.dimensions[name] = args[1]

	def num_side_ss(self,*args):
		"""
		Get/Set method for the number of faces in a side set
		If one args are passed, then it returns number of faces in the side set.
		If two args are passed it will set the number of faces in the side set to the number passed. 	  
		"""
		name = "num_side_ss"+ repr(args[0])
		if len(args) == 1:
			return self.src.dimensions[name]
		if len(args) == 2:
			self.src.dimensions[name] = args[1]
            
	def eb_prop(self,*args):
		"""
		Get/Set method for the node set ids associated with blocks.
		"""
		name = "eb_prop"+ repr(args[0])
		if len(args) == 1:
			return self.src.variables[name].getValue()
		if len(args) == 2:
			self.src.variables[name] = args[1]

	def ns_prop(self,*args):
		"""
		Get/Set method for the node set ids associated with node sets.
		"""
		name = "ns_prop"+ repr(args[0])
		if len(args) == 1:
			return self.src.variables[name].getValue()   
		if len(args) == 2:
			self.src.variables[name] = args[1]

	def ss_prop(self,*args):
		"""
		Get/Set method for the side set ids side sets.
		"""
		name = "ss_prop"+ repr(args[0])
		if len(args) == 1:
			return self.src.variables[name].getValue()     
		if len(args) == 2:
			self.src.variables[name] = args[1]

	def elem_ss(self,*args):
		"""
		Get/Set method for the elements associated with a side set.
		If one arg are passed, then it returns the elements associated with the sideset.
		If two args are passed it will set the elements associated with the side set to numpy array passed in.
		"""
		name = "elem_ss"+ repr(args[0])
		if len(args) == 1:
			return self.src.variables[name].getValue()
		if len(args) == 2:
			self.src.variables[name] = args[1]

	def side_ss(self,*args):
		"""
		Get/Set method for the element sides in the side set.
		If one arg is passed, then it returns the element sides in the side set.
		If two args ires passed it will set the the element sides in the side set to the numpy array passed. 
		"""
		name = "side_ss"+ repr(args[0])
		if len(args) == 1:
			return self.src.variables[name].getValue()
		if len(args) == 2:
			self.src.variables[name] = args[1]

	def node_ns(self,*args):
		"""
		Get/Set method for the node ids in a node set.
		If one arg is passed, then it returns the node ids in a node set.
		If two args are passed it will set the node ids in a node set to the numpy array passed.
		"""
		name = "node_ns"+ repr(args[0])
		if len(args) == 1:
			return self.src.variables[name].getValue()     
		if len(args) == 2:
			self.src.variables[name] = args[1]
			
	def node_ns_named(self,*args):
		"""
		Get/Set method for named node ids in a node set.
		If one arg is passed, then it returns the node ids in a node set.
		If two args are passed it will set the node ids in a node set to the numpy array passed.
		"""
		ns_names = self.src.variables['ns_names'].getValue()
		variableIndex = self.find_var_index(ns_names,len(ns_names),args[0])
		name = "node_ns"+str(variableIndex+1)
		if len(args) == 1:
			return self.src.variables[name].getValue()     
		if len(args) == 2:
			self.src.variables[name] = args[1]

	def dist_fact_ss(self,*args):
		"""
		Get/Set method for the distribution factor for each node in side set.
		If one arg is passed, then it returns the distribution factor for each node in side set.
		If two args are passed it will set the distribution factor for each node in side set to the numpy array passed.  
		"""
		name = "dist_fact_ss"+ repr(args[0])          
		if len(args) == 1:
			return self.src.variables[name].getValue()
		if len(args) == 2:
			self.src.variables[name] = args[1]

	def connect(self,*args):
		"""
		Returns the nodes connected to each element in the passed in block number
		"""
		name = "connect" + repr(args[0])
		if len(args) == 1:
			return self.src.variables[name].getValue()
		if len(args) == 2:
			pass

	def coord(self,*args):
		"""
		Get/Set the coordinate array for the exodus file.
		If no args are passed will return the entire coord array
		If one arg is passed will set the coord array to the passed in array.
		If two args are passed will return the entry in corresponding array.
		"""
		if len(args) == 0:
			return self.src.variables["coord"].getValue()
		if len(args) == 2:
			return self.src.variables["coord"].getValue()[args[0],args[1]]
		if len(args) == 1:
			self.src.variables["coord"] = args[0]

	def coord_named(self,*args):
		"""
		Get/Set the name specified coordinate array for the exodus file.
		If one args is passed will return the entire coord array for the name.
		If two args are passed will set the named coord array to the passed in array.
		If three args are passed will return the entry in corresponding named coordinate array.  
		"""
		name = "coord" + str(args[0])
		if len(args) == 1:
			return self.src.variables[name].getValue()
		if len(args) == 3:
			return self.src.variables[name].getValue()[args[1],args[2]]
		if len(args) == 2:
			self.src.variables[name] = args[1]

	def coor_names(self,*args):
		"""
		Get/Set the coordinate names.
		If no arguments are passed return the numpy array of numpy character arrays.
		If one argument is passed set the coor_names to the numpy array of numpy character arrays.
		If two arguments (i,j) are passed return the jth character of the ith name.
		"""
		if len(args) == 0:
			return self.src.variables["coor_names"].getValue()
		if len(args) == 2:
			return self.src.variables["coor_names"].getValue()[args[0],args[1]]
		if len(args) == 1:
			self.src.variables["coor_names"] = args[0]

	def qa_records(self,*args):
		"""
		Get/Set the qa records.
		If no arguments are passed return the numpy array of numpy character arrays.
		If one argument is passed set the qa_records to the numpy array of numpy character arrays.
		If two arguments (i,j) are passed return the jth numpy character array (a line of text) of the ith record.
		"""
		if len(args) == 0:
			return self.src.variables["qa_records"].getValue()
		if len(args) == 2:
			return self.src.variables["qa_records"].getValue()[args[0],args[1]] 
		if len(args) == 1:
			self.src.variables["qa_records"] = args[0]       

	def info_records(self,*args):
		"""
		Get/Set the info records.
		If no arguments are passed return the numpy array of numpy character arrays.
		If one argument is passed set the info_records to the numpy array of numpy character arrays.
		If two arguments (i,j) are passed return the jth character of the ith record.
		"""
		if len(args) == 0:
			return self.src.variables["info_records"].getValue()
		if len(args) == 2:
			return self.src.variables["info_records"].getValue()[arg[0],arg[1]]
		if len(args) == 1:
			self.src.variables["info_records"] = arg[0]

	def time_whole(self,*args):
		"""
		Returns the time values array.
		"""
		if len(args) == 0:
			return self.src.variables["time_whole"].getValue()
		if len(args) == 1:
			pass

	def elem_var_tab(self,*args):
		 """
		 Get/Set the element variable truth table.
		 If no args are passed, return the truth table (numpy array of length number of blocks containing numpy arrays).
		 If one arg is passed, set the truth table to the passed in value.
		 If two args (i,j) are passed, get the jth value of the ith array.
		 """
		 if len(args) == 0:
		 	return self.src.variables["elem_var_tab"].getValue()
		 if len(args) == 2:
		 	return self.src.variables["elem_var_tab"].getValue()[args[0],args[1]]
		 if len(args) == 1:
		 	self.src.variables["elem_var_tab"] = args[0]

	def vals_glo_var(self,*args):
		"""
		Get/Set values of global variables.
		If no args are passed, get the entire time history of global variables.
		If one arg is passed, set the time history of global variables to the passed in value.
		If two args (i,j) are passed, get value of the ith global variable at jth time step.
		"""
		if len(args) == 0:
			return self.src.variables["vals_glo_var"].getValue()
		if len(args) == 2:
			return self.src.variables["vals_glo_var"].getValue()[args[0],args[1]]
		if len(args) == 1:
			self.src.variables["vals_glo_var"] = args[0]

	def name_glo_var(self,*args):
		"""
		Get/Set names of global variables.
		If no args are passed, get global variables names (a numpy array of 1 numpy character array per name).
		If one arg is passed, set the global variable names to the passed in value.
		If two args (i,j) are passed, get jth character of the ith global variable name.
		"""
		if len(args) == 0:
			return self.src.variables["name_glo_var"].getValue()
		if len(args) == 2:
			return self.src.variables["name_glo_var"].getValue()[args[0],args[1]]
		if len(args) == 1:
			self.src.variables["name_glo_var"] = args[0]
        
	def vals_nod_var(self,*args):
		"""
		Get/Set the nodal variables.
		If no args are passed in, get the entire array of arrays of nodal variables.
		If one arg is passed in, set get the entire array of arrays of nodal variables to the passed in value.
		If three args (i,t,j) are passed, access the jth nodal value of the ith nodal variable at timestep t.
		"""
		if len(args) == 0:
			return self.src.variables["vals_nod_var"].getValue()
		if len(args) == 3:
			return self.src.variables["vals_nod_var"].getValue()[args[0],args[1],args[2]]
		if len(args) == 1:
			self.src.variables["vals_nod_var"] = args[0]

	def vals_nod_var_named(self,*args):
		"""
		Get/Set named nodal variables nodal variables
		If 1 args is passed in, get the entire array of arrays of nodal variables of the passed in name.
		If 2 args are passed in, set get the entire array of arrays of nodal variables of the passed in name to the passed in value.
		If 2 args (name,t) are passed in, get the nodal values at timestep t of the passed in name.
		If 3 args (name,t,i) are passed, access the ith nodal value at timestep t of the passed in name.
		"""
		variableIndex = self.find_var_index(self.name_nod_var(),len(self.name_nod_var()),args[0])
		name = "vals_nod_var"+str(variableIndex+1)
		if len(args) == 1:
			return self.src.variables[name].getValue()
		if len(args) == 3:
			return self.src.variables[name].getValue()[args[1],args[2]]
		if len(args)==2:
			if isinstance(args[1],ndarray):
				self.src.variables[name] = args[1]
			else:
				return self.src.variables[name].getValue()[args[1],:]

	def vals_elem_var_named(self,*args):
		"""
		Get/Set named nodal variables nodal variables
		If 2 args (block_id,name) are passed in, get the entire array of arrays of element variables of the passed in block and name.
		If 3 args (block_id,name,target) are passed in, set get the entire array of arrays of element variables of the passed in block and name to the passed in target.
		If 3 args (block_id,name,t) are passed in, get the element values at timestep t of the passed in block and name.
		If 4 args (block_id,name,t,i) are passed, access the ith elemental value at timestep t of the passed in block and name.
		"""
		variableIndex = self.find_var_index(self.name_elem_var(),len(self.name_elem_var()),args[1])
		name = "vals_elem_var"+str(variableIndex+1)
		name = name+"eb"+str(args[0])
		if len(args) == 2:
			return self.src.variables[name].getValue()
		if len(args) == 4:
			return self.src.variables[name].getValue()[args[2],args[3]]
		if len(args)==3:
			if isinstance(args[2],ndarray):
				self.src.variables[name] = args[2]
			else:
				return self.src.variables[name].getValue()[args[2],:]

	def name_nod_var(self,*args):
		"""
		Get/Set the names of the nodal variables.
		If no args are passed in, get the entire array of names (character arrays) of nodal variables.
		If one arg is passed in, set get the entire array of names of nodal variables to the passed in value.
		If three args (i,j) are passed, access the jth character of the ith nodal variable name.
		"""
		if len(args) == 0:
			return self.src.variables["name_nod_var"].getValue()
		if len(args) == 2:
			return self.src.variables["name_nod_var"].getValue()[args[0],args[1]]
		if len(args) == 1:
			self.src.variables["name_nod_var"] = args[0]
              
	def name_elem_var(self,*args):
		"""
		Get/Set the names of the element variables.
		If no args are passed in, get the entire array of names (character arrays) of element variables.
		If one arg is passed in, set get the entire array of names of element variables to the passed in value.
		If three args (i,j) are passed, access the jth character of the ith element variable name.
		"""
		if len(args) == 0:
			return self.src.variables["name_elem_var"].getValue()
		if len(args) == 2:
			return self.src.variables["name_elem_var"].getValue()[args[0],args[1]]
		if len(args) == 1:
			self.src.variables["name_elem_var"] = args[0]
			
	def change_nodal_vars2(self,destination,timeSteps,varNames,varVals,varTypes):
		"""
		Add a new nodal variable to the existing set.
		Takes tuples with each index having a string as the name 
		and a numpy array of dimensions number of nodes X number
		of time steps
		"""
		
		#Copy all dims for new exofile creation
		numNodeVar = len(varNames) # NOTE could error check here
		stringLength = self.len_string()
		numNewTimes = len(timeSteps)
		for d in self.dimensions.keys():
			if d == 'time_step':
				#destination.src.createDimension('time_step', self.src.dimensions['time_step'])
				destination.src.createDimension('time_step', numNewTimes)
			elif d == 'num_nod_var':
				destination.src.createDimension(d,numNodeVar)
			else:
				length = self.src.dimensions[d]
				destination.src.createDimension(d,length)

		# put in new nodal variable values
		for (index,value) in enumerate(varVals):
			valsString = 'vals_nod_var' + str(index+1)
			destination.src.createVariable(valsString,(varTypes[index]),('time_step','num_nodes'))
			tmp=destination.src.variables[valsString]
			tmp.assignValue(value)

		# put in new nodal variable names
		newVarNames = zeros((numNodeVar,stringLength),dtype='|S1')
		for (rowIndex,name) in enumerate(varNames):
			for (colIndex,char) in enumerate(name):
				newVarNames[rowIndex,colIndex] = char
		destination.src.createVariable('name_nod_var',('c'),('num_nod_var','len_string'))
		destination.src.variables['name_nod_var'].assignValue(newVarNames)
		
		# Copy all variables for new exofile creation
		stringLength = self.len_string()
		for var in self.variables.keys():
			if 'vals_nod_var' in var:
				pass
			elif var == 'name_nod_var':
				pass
			elif var == 'time_whole':
				destination.src.createVariable('time_whole',('d'),('time_step',))
				destination.src.variables['time_whole'].assignValue(timeSteps)
			elif self.src.variables[var].dimensions[0] == 'time_step': # NOTE assume all time dimensions are in first dimension
				continue
				thisvar= self.src.variables[var]
				destination.src.createVariable(var,(thisvar.typecode()),(thisvar.dimensions))
				thisvar = thisvar.getValue()
				numCol = thisvar.shape[1]
				newvar = empty((numNewTimes,numCol))
				for (newIndex,oldIndex) in enumerate(timeIndices):
					newvar[newIndex,:] = thisvar[oldIndex,:]
				destination.src.variables[var].assignValue(newvar)
			else:
				getvars = self.src.variables[var]
				vardata = getvars.getValue()
				thisvar= self.src.variables[var]
				vartype  = thisvar.typecode()
				var1 = destination.src.createVariable(var,(vartype) ,(thisvar.dimensions))
				var1.assignValue(vardata)	
				attList = dir(thisvar)
				newattlist=[]
				for i in range(len(attList)):
					if attList[i] == 'assignValue':
						pass
					elif attList[i] == 'getValue':
						pass
					elif attList[i] == 'typecode':
						pass
					else:
						newattlist.append(attList[i])
				for a in newattlist:
					attData = getattr(thisvar,a)
					setattr(var1, a, attData)
		
		# copy remaining attributes
		newattlist=[]
		for attr in dir(self.src):
			if attr not in dir(destination.src):
				newattlist.append(attr)
		for attr in newattlist:
			attData = getattr(self.src,attr)
			setattr(destination.src, attr, attData)
            
	def change_nodal_vars(self,destination,timeIndices,varNames,varVals,varTypes):
		"""
		Add a new nodal variable to the existing set.
		Takes tuples with each index having a string as the name 
		and a numpy array of dimensions number of nodes X number
		of time steps
		"""
		
		#Copy all dims for new exofile creation
		numNodeVar = len(varNames) # NOTE could error check here
		stringLength = self.len_string()
		numNewTimes = len(timeIndices)
		for d in self.dimensions.keys():
			if d == 'time_step':
				destination.src.createDimension('time_step', self.src.dimensions['time_step'])
				#destination.src.createDimension('time_step', numNewTimes)
			elif d == 'num_nod_var':
				destination.src.createDimension(d,numNodeVar)
			else:
				length = self.src.dimensions[d]
				destination.src.createDimension(d,length)

		# put in new nodal variable values
		for (index,value) in enumerate(varVals):
			valsString = 'vals_nod_var' + str(index+1)
			destination.src.createVariable(valsString,(varTypes[index]),('time_step','num_nodes'))
			destination.src.variables[valsString].assignValue(value)

		# put in new nodal variable names
		newVarNames = zeros((numNodeVar,stringLength),dtype='|S1')
		for (rowIndex,name) in enumerate(varNames):
			for (colIndex,char) in enumerate(name):
				newVarNames[rowIndex,colIndex] = char
		destination.src.createVariable('name_nod_var',('c'),('num_nod_var','len_string'))
		destination.src.variables['name_nod_var'].assignValue(newVarNames)
		
		# Copy all variables for new exofile creation
		stringLength = self.len_string()
		for var in self.variables.keys():
			if 'vals_nod_var' in var:
				pass
			elif var == 'name_nod_var':
				pass
			elif var == 'time_whole':
				oldtimes = self.time_whole()
				newtimes = empty(numNewTimes)
				for (newIndex,oldIndex) in enumerate(timeIndices):
					newtimes[newIndex] = oldtimes[oldIndex]
				destination.src.createVariable('time_whole',('d'),('time_step',))
				destination.src.variables['time_whole'].assignValue(newtimes)
			elif self.src.variables[var].dimensions[0] == 'time_step': # NOTE assume all time dimensions are in first dimension
				thisvar= self.src.variables[var]
				destination.src.createVariable(var,(thisvar.typecode()),(thisvar.dimensions))
				thisvar = thisvar.getValue()
				numCol = thisvar.shape[1]
				newvar = empty((numNewTimes,numCol))
				for (newIndex,oldIndex) in enumerate(timeIndices):
					newvar[newIndex,:] = thisvar[oldIndex,:]
				destination.src.variables[var].assignValue(newvar)
			else:
				getvars = self.src.variables[var]
				vardata = getvars.getValue()
				thisvar= self.src.variables[var]
				vartype  = thisvar.typecode()
				var1 = destination.src.createVariable(var,(vartype) ,(thisvar.dimensions))
				var1.assignValue(vardata)	
				attList = dir(thisvar)
				newattlist=[]
				for i in range(len(attList)):
					if attList[i] == 'assignValue':
						pass
					elif attList[i] == 'getValue':
						pass
					elif attList[i] == 'typecode':
						pass
					else:
						newattlist.append(attList[i])
				for a in newattlist:
					attData = getattr(thisvar,a)
					setattr(var1, a, attData)
		
		# copy remaining attributes
		newattlist=[]
		for attr in dir(self.src):
			if attr not in dir(destination.src):
				newattlist.append(attr)
		for attr in newattlist:
			attData = getattr(self.src,attr)
			setattr(destination.src, attr, attData)

	def copy_dimensions(self, destination):
		"""
		Copy all dims for new exofile creation
		"""
		for d in self.dimensions.keys():
			if d == 'time_step':
				destination.createDimension('time_step', self.time_step())
			else:
				length = self.src.dimensions[d]
				destination.createDimension(d,length)

	def copy_variable(self, destination):
		"""
		Copy all varialbes for new exofile creation
		"""
		for var in self.variables.keys():
			getvars = self.src.variables[var]
			vardata = getvars.getValue()
			thisvar= self.src.variables[var]
			vartype  = thisvar.typecode()
			var1 = destination.createVariable(var,(vartype) ,(thisvar.dimensions))
			joe = var1.assignValue(vardata)	
			attList = dir(thisvar)
			newattlist=[]
			for i in range(len(attList)):
				if attList[i] == 'assignValue':
					pass
				elif attList[i] == 'getValue':
					pass
				elif attList[i] == 'typecode':
					pass
				else:
					newattlist.append(attList[i])
			for a in newattlist:
				attData = getattr(thisvar,a)
				setattr(var1, a, attData)   

	def copy_attributes(self, destination):
		"""
		Copy all attributes for new exofile creation
		"""
		globalAttList = dir(self.src)		
		newglobalattlist=[]
		for j in range(len(globalAttList)):
			if globalAttList[j] == 'flush':
				pass
			elif globalAttList[j] == 'sync':
				pass
			elif globalAttList[j] == 'close':
				pass
			elif globalAttList[j] == 'createDimension':
				pass
			elif globalAttList[j] == 'createVariable':
				pass
			else:
				newglobalattlist.append(globalAttList[j])
		for a in newglobalattlist:
			globalAttValue = getattr(self.src, a)
			setattr(destination,a, globalAttValue)
			
	def copy_exofile(self, destination):
		"""
		This functions Creates an exact duplicate of an existing exodus file
		"""
		self.copy_dimensions(destination.src)
		self.copy_variable(destination.src)
		self.copy_attributes(destination.src)
		bool = 1
		return bool
	
### NO EDITING/TESTING BELOW
        
        def new_var_dims(self,destination,exception_list):
          """
	  Create dim for new variable
          Note: making the number of timesteps = number of time steps not unlimited
          
	  """
          for d in self.dimensions.keys():
            if d == 'time_step':
              destination.createDimension('time_step', self.time_step())
            elif d not in exception_list:
              length = self.src.dimensions[d]
              destination.createDimension(d,length)
            

          for x in range(0,len(exception_list)):
            try:
		    length = self.src.dimensions[exception_list[x]] + 1
		    #print self.src.dimensions[exception_list[x]]
		    destination.createDimension(exception_list[x],length)
	    except KeyError, e:
		    length = 1
		    destination.createDimension(exception_list[x],length)
	    except TypeError, e:
		    pass
		    #print "Need to check the size of the Timestep array"

        def new_var_vars(self, destination,exception_list):
	  """
	  Script to create new variable
          """
          for var in self.variables.keys():
            if var not in exception_list:
              getvars = self.src.variables[var]
              vardata = getvars.getValue()
              vartype  = getvars.typecode()
              createdvar = destination.createVariable(var,(vartype) ,(getvars.dimensions))
              createdvar.assignValue(vardata)
              attList = dir(getvars)
              newattlist=[]
              for i in range(len(attList)):
                if attList[i] == 'assignValue':
                  pass
                elif attList[i] == 'getValue':
                  pass
                elif attList[i] == 'typecode':
                  pass
                else:
                  newattlist.append(attList[i])
                  for a in newattlist:
                    attData = getattr(getvars,a)
                    setattr(getvars, a, attData)
                    globalAttList = dir(self.src)	
                    newglobalattlist=[]
                    for j in range(len(globalAttList)):
                      if globalAttList[j] == 'flush':
                        pass
                      elif globalAttList[j] == 'sync':
			pass
                      elif globalAttList[j] == 'close':
                        pass
                      elif globalAttList[j] == 'createDimension':
			pass
                      elif globalAttList[j] == 'createVariable':
			pass
                      else:
			newglobalattlist.append(globalAttList[j])
                        for a in newglobalattlist:
                          globalAttValue = getattr(self.src, a)
                          setattr(destination,a,globalAttValue)
                          
        def new_nod_var(self, destination, wild):
	  """
	  Script to create a new nodal variable
          """
          b = destination.variables['coord'].getValue()
          destination.time_whole = self.variables["time_whole"].getValue()
          self.time_whole = self.variables["time_whole"].getValue()
          self.time_step = self.time_whole.shape
          xold = b[0]
          yold = b[1]
          num_time_steps = self.time_step[0]
          num_nod_var    = destination.dimensions.get('num_nod_var')
          num_nodes      = destination.dimensions.get('num_nodes')
          shape = (num_time_steps, num_nod_var, num_nodes)
          new_vals_nod_var = zeros(shape, Float64)
          old_vals_nod_var = self.src.variables["vals_nod_var"].getValue()
          for ts in range(num_time_steps):
            for nv in range(num_nod_var-1):
              for node in range(num_nodes):
                new_vals_nod_var[ts][nv][node] = old_vals_nod_var[ts][nv][node]
          for ts in range(num_time_steps):
            for node in range(num_nodes):
              xvalue = xold[node]
              yvalue = yold[node]
              new_vals_nod_var[ts][num_nod_var-1][node] =  self.wild(xvalue,yvalue,ts)                    
              #print new_vals_nod_var[ts][num_nod_var-1][node]
              #print self.wild(xvalue,yvalue,ts)
          oldvar = self.src.variables.get("vals_nod_var")
          vartype = oldvar.typecode()
          dimension_names = ( "time_step", "num_nod_var","num_nodes",)
          new_var = destination.createVariable('vals_nod_var',(vartype), (dimension_names))
          assign_values = new_var.assignValue(new_vals_nod_var)

	def new_var_name(self, destination,variable,variable2,variable_dim,new_names):
	  """
	  Script to create a new name for any type of variable
          """
	  try:
		  nnv_old = self.src.dimensions[variable2]
		  nnv_new = destination.dimensions[variable2]
		  if nnv_new != nnv_old + len(new_names):
			  print "the values you have input are incorrect"
			  print  "check the dimemsions of the new variable"
			  print  "see if it has been incrametned by one"
		  else:
			  oldvar  = self.src.variables.get(variable)
			  vartype= oldvar.typecode()
			  dimension_names = (variable2,"len_string")
			  newvar = destination.createVariable(variable,(vartype),(dimension_names))
			  variable_names = []
			  nodal_vars  = self.src.variables.get(variable)
			  listing = nodal_vars.getValue()
			  lister = listing.tolist()
			  for x in lister:
				  string = ""
				  for char in range(0,33):
					  string = string + x[char]
				  variable_names.append(string)

			  for x in range(0,1):
				  string = ""
				  for char in range(0,33):
					  if char < len(new_names[0][0]):
						  string = string + new_names[0][0][char]
					  else:
						  string = string + '\x00'
				    
				  variable_names.append(string)
			  new_name_nod_var = newvar.assignValue(variable_names)
	  except KeyError, e:
		  variable_dim = 1


        def new_glo_var(self, destination):
	  """
	  Script to create a new global variable
          """
          b = destination.variables['coord'].getValue()
          destination.time_whole = self.variables["time_whole"].getValue()
          self.time_whole = self.variables["time_whole"].getValue()
          self.time_step = self.time_whole.shape
          xold = b[0]
          yold = b[1]
          num_time_steps = self.time_step[0]
          num_glo_var = destination.dimensions.get('num_glo_var')
          num_nod_var    = destination.dimensions.get('num_nod_var')
          num_nodes      = destination.dimensions.get('num_nodes')
          shape = (num_time_steps, num_glo_var)
          new_vals_glo_var = zeros(shape, Float64)
          old_vals_glo_var = self.variables["vals_glo_var"].getValue()
          for ts in range(num_time_steps):
            for igv in range(num_glo_var-1):
              new_vals_glo_var[ts][igv] = old_vals_glo_var[ts][igv]
              good_list = []
              ts_list = []
              val_list = []
              for i in range(num_nod_var):
                jack =  name_nod_var[i,:]
                joan = jack.tostring()
                jill = str.rstrip(joan)
                t=str.index(joan, '\000')
                john = jill[:t]
                good_list.append(john)
		goodindex = good_list.index(nodal_variable_name)
		for ts in range(self.time_step[0]):
                  ts_list.append(ts+1)
                  vals_nod_var = e.variables["vals_nod_var"].getValue()		
                  num_nodes = e.dimensions["num_nodes"]
                  self.time_whole = ExoFile.variables["time_whole"].getValue()
                  self.time_step = self.time_whole.shape
		for node in range(num_nodes):
			for ts in range(num_time_steps):
				val_list.append(vals_nod_var[ts][goodindex][node])
				if ts == self.time_step[0]-1:
					max_val = max(val_list)										
					max_index =  val_list.index(max_val)
					min_val = min(val_list)
					min_index = val_list.index(min_val)
					val_list[:] = []
				else:
					pass
		val_list = []
		for ts in range(self.time_step[0]):
			for node in range(0,94):
				val_list.append(e.nodal_result(nodal_variable_name, ts, node))
				if ts == self.time_step[0]-1:
					max_val = max(val_list)										
					new_vals_glo_var[ts][vals_glo_var-1]= max_val
					val_list[:] = []
				else:
					pass
		oldvar = self.variables.get("vals_glo_var")
		vartype = oldvar.typecode()
		dimension_names = ( "time_step", "num_glo_var",)
		new_var = destination.createVariable('vals_glo_var',(vartype), (dimension_names))
		assign_values = new_var.assignValue(new_vals_glo_var)


        def new_nodal_var(self,destination,var_name):
	  """
	  script to create a new nodal variable
          """
          e.new_var_dims(destination,['num_nod_var'])
          e.new_var_vars(destination,['vals_nod_var','name_nod_var'])
          e.new_var_name(destination,'name_nod_var','num_nod_var',e.num_nod_var(),[var_name])
	  wilds = 1
          e.new_nod_var(destination,wilds)
          e.close()
          destination.close()

        def new_glo_var(self,destination,var_name):
          """
          Needs to beta tested and must work!!
          Havent Tried Yet
          """
          e.new_var_dims(destination,['num_nod_var'])
          e.new_var_vars(destination,['vals_nod_var','name_nod_var'])
          e.new_var_name(destination,'name_nod_var','num_nod_var',e.num_nod_var(),[var_name])
	  wilds = 1
          e.new_nod_var(destination,wilds)
          e.close()
          destination.close()

        def elem_bases(self, var_number, element_block_number, element_number):
           """
	   Generic Elemental Variable Function
           """
           var_number_st = repr(var_number)
           element_block_number_st = repr(element_block_number)
           vals_elem_var = "vals_elem_var"+var_number_st+"eb"+element_block_number_st
           self.vals_elem_var = self.src.variables[vals_elem_var]
           var_number_st = repr(var_number)
           element_block_number_st = repr(element_block_number)
           num_el_in_blk = "num_el_in_blk"+element_block_number_st
           self.num_el_in_blk = self.src.dimensions[num_el_in_blk]

	def run2dmethod(self,matrix):
	        """
	        Generic method for all 2d transformations
                """
		e2 = zeros((self.num_nodes()), Float)
		e3 = zeros((self.num_nodes()), Float)
		for node in arange(0, self.num_nodes()):
			xvalue= self.coord()[0,node]	
			yvalue= self.coord()[1,node]
                        xycoords = array(([xvalue],[yvalue]))
 			reshapedcoords = reshape(xycoords, (2,1))
                        print "reshape is",reshapedcoords.shape
                        print "the matrix shape is",matrix.shape
 			function=matrixmultiply(matrix,reshapedcoords)
			newx= function[0]
			newy= function[1]
			e2[node] = newx[0]
			e3[node] = newy[0]
		data = array([e2, e3])
                self.src.variables["coord"] = data

	def run3dmethod(self,matrix):
	        """
	        Generic method for all 3d transformations
                """
		e2 = zeros((self.num_nodes()), Float)
		e3 = zeros((self.num_nodes()), Float)
		e4 = zeros((self.num_nodes()), Float)
		for node in arange(0, self.num_nodes()):
			xvalue= self.coord()[0,node]	
			yvalue= self.coord()[1,node]
			zvalue= self.coord()[2,node]
			xycoords = array([xvalue,yvalue,zvalue,1])
			reshapedcoords = reshape(xycoords, (4,1))
			function=matrixmultiply(matrix1,reshapedcoords)
			newx= scalefunction[0]
			newy= scalefunction[1]
			newz= scalefunction[2]
			e2[node] = newx[0]
			e3[node] = newy[0]
			e4[node] = newz[0]
		data = array([e2,e3,e4])
		self.coord[:] = data
		ExoFile.close()

        def scale(*args):
            """
            Method to scale the deformation by the given parameters
            """
            self = args[0]
            if len(args) == 3:
                x = args[1]
                y = args[2]
                matrix = array([[x,0],[0,y]])
                self.run2dmethod(matrix)
                self.close()
            elif len(args) == 4:
                x = args[1]
                y = args[2]
                z = args[3]
                matrix = array([[x,0,0],[0,y,0],[0,0,z]])
                self.run3dmethod(matrix)
                self.ExoFile.close()
            else:
                assert 1<len(args)<4		


	def rotation(*args):
            """
            Method to rotate the deformation by the given parameters
            """
            self = args[0]
            if len(args) == 2:
                rd = args[1]
                matrix= array([[cos(rd),-sin(rd)],[sin(rd),cos(rd)]])
                self.run2dmethod(matrix)
                self.ExoFile.close()
            elif len(args) == 3:
                x,y,z == args
            else:
                assert 0 <len(args) < 4	

	def shear(*args):
            """
            Method to shear the deformation by the given parameters
            """
            self = args[0]
            if len(args) == 3:
                x = args[1]
                y = args[2]
                matrix= array([[1,x,0],[y,1,0], [0,0,1]])
                e2 = zeros((self.num_nodes()), Float)
                e3 = zeros((self.num_nodes()), Float)
                for node in arange(0, self.num_nodes()):
                    xvalue= self.coord()[0,node]	
                    yvalue= self.coord()[1,node]
                    print xvalue
                    print yvalue
                    xycoords = array(([xvalue],[yvalue],[1]))
                    reshapedcoords = reshape(xycoords, (3,1))
                    function=matrixmultiply(matrix,reshapedcoords)
                    newx= function[0]
                    newy= function[1]
                    e2[node] = newx[0]
                    e3[node] = newy[0]
                    data = array([e2, e3])
                self.src.variables["coord"] = data
                self.src.close()

            elif len(args) == 4:
                sx = args[1]
                sy = args[2]
                sz = args[3]
                if 4 == x:
                    matrix = array([[1,0,0,0],[sy,1,0,0],[sz,0,1,0],[0,0,0,1]])
                    self.run3dmethod(matrix)
                    self.ExoFile.close()
                elif 4 == y:
                    matrix = array([[1,sx,0,0],[0,1,0,0],[0,sz,1,0],[0,0,0,1]])
                    self.run3dmethod(matrix)
                    self.ExoFile.close()	 
                elif 4 == z:
                    matrix = array([[1,0,sx,0],[0,1,sy,0],[0,0,1,0],[0,0,0,1]])
                    self.run3dmethod(matrix)
                    self.ExoFile.close()	
                else:
                    print "You must specify which direction to shear in, x, y,z"
				
            else:
                assert 1  <len(args) < 5	

	def reflection(*args):
            """
            Method to reflect the deformation by the given parameters
            """
            self = args[0]
            if len(args) == 4:
                if args[3] == "x":
                    matrix = array([[1,0],[0,-1]])
                    self.run2dmethod(matrix)
                    self.ExoFile.close()
                elif args[3] == "y":
                    matrix = array([[1,0],[0,-1]])
                    self.run2dmethod(matrix,matrixoperation)
                    self.ExoFile.close()
                else:
                    print "you must specifiy around which axis you want to rotate"

            elif len(args) == 5:
                if args[5] == x: 
                    matrix = array([[1,0,0,0],[0,cos(r),-sin(r),0],[0,sin(r),cos(r),0],[0,0,0,1]])
                    self.run3dmethod(matrix,matrixoperation)
                    self.ExoFile.close()
                elif args[5] == y:
                    matrix = array([[cos(r),0,sin(r),0],[0,1,0,0],[-sin(r),0,cos(r),0],[0,0,0,1]])
                    self.run3dmethod(matrix,matrixoperation)
                    self.ExoFile.close()
                elif args[5] == z:
                    matrix = array([[cos(r),-sin(r),0,0],[sin(r),cos(r),0,0],[0,0,1,0],[0,0,0,1]])
                    self.run3dmethod(matrix,matrixoperation)
                    self.ExoFile.close()			
                else:
                    print "you must specifiy around which axis you want to rotate for the last arg"
            else:
                print " error your dims dont match anything 1  < %d  < 6",len(args)	

	def translation(*args):
            """
            Method to translate the deformation by the given parameters
            """
            if len(args) == 3:
                x = args[1]
                y = args[2]
                e2 = zeros((self.num_nodes()), Float)
                e3 = zeros((self.num_nodes()), Float)
                for node in arange(0, self.num_nodes()):
                    xvalue= self.coord()[0,node]	
                    yvalue= self.coord()[1,node]
                    xycoords = array([xvalue,yvalue])
                    reshapedcoords = reshape(xycoords, (2,1))
                    translate= array([x,y])
                    complete=translate+reshapedcoords
                    newx = complete[0]
                    newy = complete[1]
                    e2[node] = newx[0]
                    e3[node] = newy[0]
                    data = array([e2, e3])
                    self.coord[:] = data
                    self.close()

            elif len(args) == 4:
                x = args[1]
                y = args[2]
                z = args[3]
                matrix = array([[1,0,0,x],[0,1,0,y],[0,0,1,z],[0,0,0,1]])
                self.run3dmethod(matrix)
                self.close()
            else:
                assert 1  <len(args) < 3

	def reflect_about_a_line(self,m,b):
	        """
		Deforms the mesh around a line
                """
		e2 = zeros((self.num_nodes()), Float)
		e3 = zeros((self.num_nodes()), Float)
		for node in arange(0, self.num_nodes()):
			xvalue= self.coord()[0,node]	
			yvalue= self.coord()[1,node]
			newx = (2*m*yvalue- (m*m-1)*xvalue-2*b)/(1+m*m)
			newy = ((m*m-1)*yvalue-2*m*xvalue+2*b)/(1+m*m)
			e2[node] = newx
			e3[node] = newy
		data = array([e2,e3])
		self.coord[:] = data
		self.close()

       	def twist(self,T,B,b,c,G):
	  """
	  does a twist deformation on the exofile 
          """
          e2 = zeros((self.num_nodes()), Float)
          e3 = zeros((self.num_nodes()), Float)
          e4 = zeros((self.num_nodes()), Float)
          xlist = []
          ylist = []
          zlist = []
          for node in arange(0, self.num_nodes()):
            xvalue= self.coord()[0,node]
            xlist.append(xvalue)
            yvalue= self.coord()[1,node]
            ylist.append(yvalue)
            zvalue = self.coord()[2,node]
            zlist.append(zvalue)
          max_val = max(zlist)
          max_index = zlist.index(max_val)
          min_val = min(zlist)
          min_index = zlist.index(min_val)
          for x in range(0,len(zlist)):
            distanceL = (zlist[min_index]-zlist[x])	
            distancedy = (ylist[min_index]-ylist[x])
            distancedx = (xlist[min_index]-xlist[x])			
            oldx = self.coord()[0,x]
            oldy = self.coord()[1,x]
            oldz = self.coord()[2,x]
            L = max_val - oldz
            P =  (T*L)/(B*b*(c*c*c)*G)
            matrix = array([[cos(P),-sin(P),0],[sin(P),cos(P),0],[0,0,1]])
            xycoords = array([oldx,oldy,oldz])			
            reshapedcoords = reshape(xycoords, (3,1))
            function = matrixmultiply(matrix,reshapedcoords)
            newx= function[0]
            newy= function[1]
            newz= function[2]
            e2[x] = newx[0]
            e3[x] = newy[0]
            e4[x] = newz[0]
          data = array([e2,e3,e4])
          self.coord()[:] = data
          self.close()

	def deflection(self,l,b,h,f,e):
	  """
	  Deflects the exofile... needs to be error checked...
          """
          F = float(f)
          B = float(b)
          E = float(e)
          L = float(l)
          H = float(h)
          e2 = zeros((self.num_nodes()), Float)
          e3 = zeros((self.num_nodes()), Float)
          e4 = zeros((self.num_nodes()), Float)
          xlist = []
          ylist = []
          zlist = []
          print "The coord shape is",self.coord().shape
          for node in arange(0, self.num_nodes()):
              
              xvalue= self.coord()[0,node]
              xlist.append(xvalue)	
              yvalue= self.coord()[1,node]
              ylist.append(yvalue)
              zvalue = self.coord()[1,node]
              zlist.append(zvalue)
              I = float((B*H*H*H)/12)
          for node in range(0,len(zlist)):
              oldx = float(self.coord()[0,node])
              oldy = float(self.coord()[1,node])
              oldz = float(self.coord()[2,node])
              x = oldz
              v = float(((-F*x*x)*(3*L-x))/(6*E*I))
              testf = float(x - v)
              e2[node] = oldx
              e3[node] = testf
              e4[node] = oldz
          data = array([e2,e3,e4])
          self.coord()[:] = data
          
          self.close()
        
	def get_coordinates(*args):
          """
          Given the node and number of demensions of the coords array.
          Will return the physicall location of a node
          """
	  self = args[0]
          coord_list = []
          if args[2] == 2:
            xvalue= self.coord()[0,args[1]]	
            yvalue= self.coord()[1,args[1]]
            coord_list.append(xvalue)
            coord_list.append(yvalue)
            return coord_list
          if args[2] == 3:
            xvalue= self.coord()[0,args[1]]	
            yvalue= self.coord()[1,args[1]]
            zvalue = self.coord()[2,args[1]]
            coord_list.append(xvalue)
            coord_list.append(yvalue)            
            coord_list.append(zvalue)
            return coord_list
          else:
            print "Error you must pass a node and how many dimensions the array is"

        def strip_nulls(self,variable_names,variable_dim):
          """
          Params:
          var_name is an array of the variable names
          var_dim is the number of elements in the array

          Result:
          Returns an array with all the nulls characters stripped
          """
	  good_list = []
	  for x in range(0,variable_dim):
		  varname =  variable_names[x,:]
		  var_as_string = varname.tostring()
		  strip_string = str.rstrip(var_as_string)
		  t=str.index(var_as_string, '\000')
		  index = strip_string[:t]
		  good_list.append(index)
	  return good_list
      
        def get_numeric_id(self,array1,idkey):
          """
          Params-
          array = an array of names descrbing the element
          idkey = the id name to be matched

          Result-
          Returns the key to be matched
          note i am assuming that the array passed is a list,
          therefore converting it into an array
          """

	  bool = 0
	  for y in range(0,len(array1)):
	  	x = array1[y]
		if x == idkey:
			return y
	  	else:
			pass
	  if bool == 0:
		  print "not in array passed"
		  return -1
	  else:
		  pass

      
        def find_var_index(self,elem_var,elem_dim,elem_key):
          """
          Params:
          elem_var is an array of the element names
          elem_dim is an array of the number of element dims
          elem_key is the name you want to match

          Result:
          Returns the index of the key
          """
          bool = 0
          good_list = self.strip_nulls(elem_var,elem_dim)
	  for x in range(0,elem_dim):
		  if good_list[x] == elem_key:
			  bool = 1
			  return x
		  else:
			  pass
	  if bool == 0:
		  print elem_key, "not in list"
		  return -1
	  else:
		  pass


      
#         def unittests(self):
#             testfile = open("out.txt",'w')
#             testfile.write("Num Nodes" + '\t' + '\t'  + str(e.num_nodes()) + '\n')
#             testfile.write("Num Elem" + '\t' + '\t' + str(e.num_elem()) + '\n')
#             testfile.write("Num Sidesets" + '\t' + '\t' + str(e.num_side_sets()) + '\n')
#             testfile.write("Num NodeSets" + '\t' + '\t' + str(e.num_node_sets()) + '\n')
#             testfile.write("Num Qa Records" + '\t' + '\t' + str(e.num_qa_rec()) + '\n')
#             testfile.write("Num Info" + '\t' + '\t' + str(e.num_info()) + '\n')
#             testfile.write("Num Glo_Var" + '\t' + '\t' + str(e.num_glo_var()) + '\n')
#             testfile.write("Num Nod_Var" + '\t' + '\t' + str(e.num_nod_var()) + '\n')
#             testfile.write("Num Time_Steps" + '\t' + '\t' + str(e.time_step()) + '\n')
#             testfile.write("String_Lenth" + '\t' + '\t' + str(e.len_string()) + '\n')
#             testfile.write("Line_Lenth" + '\t' + '\t' + str(e.len_line()) + '\n')
#             testfile.write("num_nod_per_el1" + '\t' + '\t' + str(e.num_nod_per_el(1)) + '\n')
#             testfile.write("num_el_in_blk1" + '\t' + '\t' + str(e.num_el_in_blk(1)) + '\n')
#             testfile.write("Num_Sides_in_SS1" + '\t' + '\t' + str(e.num_side_ss(1)) + '\n')
#             testfile.write("Eb_Prop_1" + '\t' + '\t' + str(e.eb_prop(1)) + '\n')
#             testfile.write("NS_Prop_1" + '\t' + '\t' + str(e.ns_prop(1)) + '\n')
#             testfile.write("Elem_SS" + '\t' + '\t' + str(e.elem_ss(1)) + '\n')
#             testfile.write("Side_SS" + '\t' + '\t' + str(e.side_ss(1)) + '\n')
#             testfile.write("node_ns" + '\t' + '\t' + str(e.node_ns(1)) + '\n')
#             testfile.write("dist_fact_ns" + '\t' + '\t' + str(e.dist_fact_ss(1)) + '\n')
#             testfile.write("connect" + '\t' + '\t' + str(e.connect(1)) + '\n')
#             testfile.write("time_whole" + '\t' + '\t' + str(e.time_whole()) + '\n')
#             testfile.write("vals_glo_var" + '\t' + '\t' + str(e.vals_glo_var().shape) + '\n')
#             testfile.write("vals_nod_var" + '\t' + '\t' + str(e.vals_nod_var().shape) + '\n')
#             testfile.write("name_nod_var" + '\t' + '\t' + str(e.name_nod_var().shape) + '\n')
#             testfile.write("name_glo_var" + '\t' + '\t' + str(e.name_glo_var().shape) + '\n')

            #e.nodeset([30176],['VX'],1,1)   
            #dir = "/home2/veuria/.gnome-desktop/OldDesktop/rehogan/"
            #self.search_dir_script(dir)
            #destination = NetCDFFile("NewExofile.exoII", "w")
            #e = ExoFile('dropout2.exoII','a')
            #destination = NetCDFFile("NewExofile.exoII", "w")

            #testfile.write("vals_elem_var" + '\t' + '\t' + str(e.vals_elem_var().shape) + '\n')
            #testfile.write("elem_var_tab" + '\t' + '\t' + str(e.elem_var_tab()) + '\n')
            #testfile.write("info_records" + '\t' + '\t' + str(e.info_records)) + '\n')
            #testfile.write("qa_records" + '\t' + '\t' + str(e.qa_records()) + '\n')
            #testfile.write("coord_names" + '\t' + '\t' + str(e.coor_names()) + '\n')
            #coord names having problems printing out as strings add and fix
            #testfile.write("Num Elem_Var" + '\t' + '\t' + str(e.num_elem_var()) + '\n')
            
        def new_idea(self,destination,vardata,var):
	  """
	  Returns the time values array.
          """
          try:
            getvars 	=	self.src.variables[var]
            vartype  	=	getvars.typecode()
            vardata_real 	= 	vardata.typecode()
            createdvar 	= 	destination.createVariable(var,(vardata_real) ,(getvars.dimensions))
            createdvar.assignValue(vardata)
            attList = dir(getvars)
            newattlist=[]
            for i in range(len(attList)):
              if attList[i] == 'assignValue':
                pass
              elif attList[i] == 'getValue':
                pass
              elif attList[i] == 'typecode':
                pass
              else:
                newattlist.append(attList[i])
                print "The att list is ",attList[i]
              
            for a in newattlist:
              attData = getattr(getvars,a)
              print attData
              setattr(getvars, a, attData)
            globalAttList = dir(self.src)	
            newglobalattlist=[]
            for j in range(len(globalAttList)):
              if globalAttList[j] == 'flush':
                pass
              elif globalAttList[j] == 'sync':
                pass
              elif globalAttList[j] == 'close':
                pass
              elif globalAttList[j] == 'createDimension':
                pass
              elif globalAttList[j] == 'createVariable':
                pass
              else:
                newglobalattlist.append(globalAttList[j])
            for a in newglobalattlist:
              globalAttValue = getattr(self.src, a)
              setattr(destination,a,globalAttValue)	
          except KeyError, e:
            print "There are no variables of this type: ",var


        def copy_dimensions_for_slice(self,destination,exception_list):
	  """
	  Returns the time values array.
          """
          for d in self.dimensions.keys():
	    print "i am on dim",d
            if d not in exception_list:
              length = self.src.dimensions[d]
              destination.createDimension(d,length)

        def rest_of_dims_for_slice(self,destination,exception_list):
	  """
	  Returns the time values array.
          """
          for d in self.dimensions.keys():
            if d in exception_list:
              length = 1
              destination.createDimension(d,length)

        def new_vars_slicing(self,destination,filename,exception_list):
	  """
	  Returns the time values array.
	  Note only supports 99< element blocks..... need to update it....
          """
          for var in self.variables.keys():
            if var in exception_list:
              try:
	        print "i am on var",var
                getvars = self.src.variables[var]
                if var == 'vals_nod_var':
		  vardata = self.src.variables[var][1:2,:]
		  #vardata = self.vals_nod_var()[1:2 ,: , :]
                  self.new_idea(destination,vardata,var)
                elif var == 'vals_glo_var':
		  vardata = self.src.variables[var][1:2,:]
		  #vardata = self.vals_glo_var()[1:2,:]
		  self.new_idea(destination,vardata,var)
                elif var == 'time_whole':
                  dim =  ('time_step',)
                  vardata = self.src.variables[var].getValue()
                  vartype  = getvars.typecode()
                  createdvar = destination.createVariable(var,(vartype),(dim))
                  createdvar.assignValue(vardata[1])
                  attList = dir(getvars)
                  newattlist=[]
                  for i in range(len(attList)):
                    if attList[i] == 'assignValue':
                      pass
                    elif attList[i] == 'getValue':
                      pass
                    elif attList[i] == 'typecode':
                      pass
                    else:
                      newattlist.append(attList[i])
                      print "!@%!@#$!@#$!@#$!@#$!@#$!@#",attList[i]
                  for a in newattlist:
                    attData = getattr(getvars,a)
                    setattr(destination, a, attData)
                    print "The att data is",attData
                else:
			vardata = self.src.variables[var][1:2,:]
			self.new_idea(destination,vardata,var)
			
              except KeyError, e:
		      pass
                #print "There are no variables of this type: ",var

	def elem_var(self,destination):
		#try:
		#	var_name = 'time_step'
		#	length = 1
		#	destination.createDimension(var_name,length)
		#except IOError,e:
		#	pass
#		for eb in range(1,2):		
		for eb in range(1,self.num_el_blk()):
#			for var in range(1,10):
			for var in range(1,self.num_elem_var()):			
				var_num_st = repr(var)
				eb_num_st = repr(eb)
			        vals_elem_var = "vals_elem_var"+var_num_st+"eb"+eb_num_st
				self.vals_elem_var = self.src.variables[vals_elem_var]
				num_el_in_blk = "num_el_in_blk"+eb_num_st
				self.num_el_in_blk = self.src.dimensions[num_el_in_blk]
				#try:
				#	destination.createDimension(num_el_in_blk, self.num_el_in_blk)
				#except IOError,e:
				#	pass
				#print "on", vals_elem_var
				getvars = self.src.variables[vals_elem_var][1:2,:]
				print getvars.shape
				vardata = getvars
				var1 = destination.createVariable(vals_elem_var,
								  self.src.variables[vals_elem_var].typecode(),
								  self.src.variables[vals_elem_var].dimensions)
				var1.assignValue(vardata)

	def timetest(self):
		now = time.localtime(time.time())
		print time.asctime(now)

		
        def subsliced_exofile(self,destinationf,filename):
	  """
	  Returns the time values array.
          """
	  self.timetest()
	  print self.num_elem_var()
          exception_list = []
	  
          try:
            num_blocks = self.src.dimensions["num_el_blk"]
	    print num_blocks
            for var in range(0,self.num_elem_var()):
              for eb in range(0,num_blocks):
                name = "vals_elem_var"+repr(var+1)+"eb"+repr(eb+1)
                exception_list.append(name)
          except KeyError, e:
            print "There are no variables of this type: Vals Elem Var"

          try:
            self.name_glo_var()
            exception_list.append("vals_glo_var")
          except KeyError, e:
            print "There are no variables of this type: Vals Glo Var"
          try:
            self.name_nod_var()
            exception_list.append("vals_nod_var")
          except KeyError, e:
            print "There are no variables of this type: Vals Nod Var"
          try:
            self.time_whole()
            exception_list.append("time_whole")
          except KeyError, e:
            print "There are no variables of this type: Time_Whole"
          print exception_list


          self.copy_dimensions_for_slice(destination,['time_step'])
          self.rest_of_dims_for_slice(destination,['time_step'])
	  self.new_var_vars(destination,exception_list)
          self.new_vars_slicing(destination,filename,exception_list)
	  self.elem_var(destination)
	  self.timetest()



	def extrude(self,destination, destination2,  array, delta, side_set = 0):
		glo_var = 0
		nod_var = 0
		elem_var = 0
		side_sets = 0
		node_set = 0
		num_elem = 0
		xlist = []
		ylist = []
		zlist = []

		for y in range(0,6):
			for x in range(0,6):
				xlist.append(x)
				ylist.append(y)
				
		connect1_data = []
		connectlist = []
		array = []
		list2 = []
		list2.append(xlist)
		list2.append(ylist)
		xlist2 = []
		ylist2 = []
		print "orginal len is",len(list2[0])
		for coord in range(0,len(list2[0])):
			xlist2.append(xlist[coord])
			ylist2.append(ylist[coord])
			zlist.append(0)
		print "orginal len is",len(xlist)
		for coord in range(0,len(list2[0])):
			xlist2.append(xlist[coord])
			ylist2.append(ylist[coord])
			zlist.append(1)
		array.append(xlist2)
		array.append(ylist2)
		array.append(zlist)
		list = []
		list = array
		num_dim = 3
	        num_nodes = len(xlist2)
		print "num_nodes",num_nodes
		max = int(sqrt(num_nodes/2)) 
		print "max is",max
		for n in range(0,len(xlist2)):
			n = n + 1
			if n > num_nodes/2-max:
				break
			if n%max == 0:
				pass
			else:
				list2 = []
				first = int(n)
				second = int(n+1)
				third = int(n +max + 1)
				forth = int(n + max)
				fifth = int(n + num_nodes/2)
				sixth = int(n + num_nodes/2 + 1) 
				seventh = int(n + num_nodes/2 + max + 1) 
				eighth  = int(n + num_nodes/2 + max )
				list2.append(first)
				list2.append(second)
				list2.append(third)
				list2.append(forth)
				list2.append(fifth)
				list2.append(sixth)
				list2.append(seventh)
				list2.append(eighth)
				connect1_data.append(list2)
				num_elem = num_elem + 1
				if n > num_nodes-max-2:
					break	
		num_att_in_blk = 0
		num_df_ns = 0
		num_aq_rec = 0
		num_info = 0
		dims = {'num_nodes' : len(xlist2),
			'num_dim' : 3,
			'num_elem' : num_elem,
			'num_el_blk' : 1,
			'num_el_in_blk1' : num_elem,
			'num_nod_per_el1': 8,
			'num_qa_rec' : 1,
			'time_step' : 0,
			'len_string' : 33,
			'len_line' : 81,
			'four' : 4,
			}
		for dim, length in dims.iteritems():
			self.create_dim(destination,dim,length)	

		coord_dims = ('num_dim', 'num_nodes',)
		coord_data = list
		var = destination.createVariable('coord','d',(coord_dims))
		var.assignValue(coord_data)
		coor_names_dims = ('num_dim', 'len_string',)
		coor_names_data = ['x',
				   'y',
				   'z                                ']
		var = destination.createVariable('coor_names',self.typedefine(coor_names_data[1]),(coor_names_dims))
		var.assignValue(coor_names_data)

		thisvar= self.src.variables['connect1']
		vartype  = thisvar.typecode()
		connect_dim = ('num_el_in_blk1','num_nod_per_el1',)
		CONNECT1 = destination.createVariable('connect1','i',(connect_dim))
		CONNECT1.assignValue(connect1_data)		
		thisvar= destination.variables['connect1']
		
		attribut_dim = ('num_el_in_blk', 'num_att_in_blk',)
		eb_prop_dim = ('num_el_blk',)
		elem_map_dim = ('num_elem',)
		qa_records_dim = ('num_qa_rec', 4, 'len_string',)
		info_records_dim = ('num_info', 'len_line',)
		elem_var_tab = ('num_el_blk', 'num_elm_var',)
		eb_prop1_data = []
		print "4"

		for eb in range(0,dims['num_el_blk']):
			eb = eb + 1
			eb_prop1_data.append(eb)
		eb_prop1_dim = ('num_el_blk',)
		var = destination.createVariable("eb_prop1",'i' ,eb_prop1_dim)
		var.assignValue(eb_prop1_data)
		setattr(var,'name',"ID")
		eb_status_data = []
		for eb in range(0,dims['num_el_blk']):
			eb_status_data.append(1)
		eb_status_dim = ('num_el_blk',)
		var = destination.createVariable("eb_status",'i' ,eb_status_dim)
		print "5"
		var.assignValue(eb_status_data)
		elem_map_data = []
		for elem in range(0,dims['num_elem']):
			elem = elem + 1
			elem_map_data.append(elem)
		elem_map_dim = ('num_elem',)
		var = destination.createVariable("elem_map",'i' ,elem_map_dim)
		var.assignValue(elem_map_data)
		print "6"
		elem_num_map_data = []
		for elem in range(0,dims['num_elem']):
			elem = elem + 1
			elem_num_map_data.append(elem)
		elem_num_map_dim = ('num_elem',)
		var = destination.createVariable("elem_num_map",'i' ,elem_num_map_dim)
		var.assignValue(elem_num_map_data)
		node_num_map_data = []
		for node in range(0,dims['num_nodes']):
			node = node + 1
			node_num_map_data.append(node)
		node_num_map_dim = ('num_nodes',)
		var = destination.createVariable("node_num_map",'i' ,node_num_map_dim)
		var.assignValue(node_num_map_data)
		qa_records_dim = ('num_qa_rec', 'four', 'len_string',)
		qa_records_data = ["cubit"]

		api = zeros((1,), Float32)
		api[0] = 4.01000023
		ver = zeros((1,), Float32)
		ver[0] = 3.00999999

		atts = {
			'api_version' : api ,
			'version' : ver,
			'floating_point_word_size' :  [8] ,
			'file_size' : [0] ,
			'title' : "One element box" 
			}
		print "here i am "
		for att, value in atts.iteritems():
			setattr(destination,att,value)	
		setattr(CONNECT1,"elem_type","QUAD8")
		time_whole_dims = ('time_step',)
		time_whole_data = 0
		print "i got here"
		var = destination.createVariable('time_whole',self.typedefine(time_whole_data),(time_whole_dims))
		var.assignValue(time_whole_data)

		qa_records_data = ["Cubit"]
		var = destination.createVariable("qa_records",'c' ,qa_records_dim)
		var.assignValue(qa_records_data)
		destination.close()		

	def hex27(self,destination,array,delta,side_set = 0):
		exodus_results = 1
		## inital node reunumbering
		new_eb = 6
		num_div = (2 * new_eb + 1)
		delta = 500000. #1000000. / 2
		maxz = 3
		num_nodes = self.num_nodes() * num_div
		new_coord_data = zeros((3, num_nodes), Float32)
		for node in range(0,self.num_nodes()):
			for offset in range(0,num_div):
				x1 = self.src.variables["coord"].getValue()[0,node] 
				y1 = self.src.variables["coord"].getValue()[1,node]
				r = sqrt(pow(x1,2) + pow(y1,2))
				#new_coord_data[0][node + self.num_nodes() * offset] = x1 #r * cos(30 * offset * (pi/180)) 
				#new_coord_data[1][node + self.num_nodes() * offset] = y1 #r * sin(30 * offset * (pi/180)) 
				#new_coord_data[2][node + self.num_nodes() * offset] = delta * offset #y1
				new_coord_data[0][node + self.num_nodes() * offset] = r * cos(30 * offset * (pi/180)) 
				new_coord_data[1][node + self.num_nodes() * offset] = r * sin(30 * offset * (pi/180)) 
				new_coord_data[2][node + self.num_nodes() * offset] = x1 *5
		new_connect_data =  zeros((self.num_el_in_blk(1) * new_eb, 27), Int)
		for elem in range(0,self.num_el_in_blk(1)):
			for node in range(0,self.num_nodes()):
				for offset in range(0,new_eb):
					if offset > 0:
						#firstdim 
						if node == 0:
							base = self.src.variables["connect1"].getValue()[elem,node]
							firstdim = base + self.num_nodes() * (2 * offset + 0)
							secondim = base + self.num_nodes() * (2 * offset + 1)
							thirddim = base + self.num_nodes() * (2 * offset + 2)
							new_connect_data[elem + self.num_el_in_blk(1)* offset][node] = firstdim 
							new_connect_data[elem + self.num_el_in_blk(1) * offset][13-1] = seconddim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][5-1] = thirddim 

						if node == 1:
							base = self.src.variables["connect1"].getValue()[elem,node]
							base = self.src.variables["connect1"].getValue()[elem,node]
							firstdim = base + self.num_nodes() * (2 * offset + 0)
							secondim = base + self.num_nodes() * (2 * offset + 1)
							thirddim = base + self.num_nodes() * (2 * offset + 2)
							new_connect_data[elem + self.num_el_in_blk(1) * offset][node] = firstdim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][14-1] = seconddim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][6-1] = thirddim 
							
						if node == 2:
							base = self.src.variables["connect1"].getValue()[elem,node]
							firstdim = base + self.num_nodes() * (2 * offset + 0)
							secondim = base + self.num_nodes() * (2 * offset + 1)
							thirddim = base + self.num_nodes() * (2 * offset + 2)
							new_connect_data[elem + self.num_el_in_blk(1) * offset][node] = firstdim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][15-1] = seconddim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][7-1] = thirddim 
							
						if node == 3:

							base = self.src.variables["connect1"].getValue()[elem,node]
							firstdim = base + self.num_nodes() * (2 * offset + 0)
							secondim = base + self.num_nodes() * (2 * offset + 1)
							thirddim = base + self.num_nodes() * (2 * offset + 2)
							new_connect_data[elem + self.num_el_in_blk(1) * offset][node] = firstdim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][16-1] = seconddim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][8-1] = thirddim 
							
						if node == 4:
							
							base = self.src.variables["connect1"].getValue()[elem,node]
							firstdim = base + self.num_nodes() * (2 * offset + 0)
							secondim = base + self.num_nodes() * (2 * offset + 1)
							thirddim = base + self.num_nodes() * (2 * offset + 2)
							new_connect_data[elem + self.num_el_in_blk(1) * offset][9-1] = firstdim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][21-1] = seconddim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][17-1] = thirddim
							
						if node == 5:

 							base = self.src.variables["connect1"].getValue()[elem,node]
							firstdim = base + self.num_nodes() * (2 * offset + 0)
							secondim = base + self.num_nodes() * (2 * offset + 1)
							thirddim = base + self.num_nodes() * (2 * offset + 2)
							new_connect_data[elem + self.num_el_in_blk(1) * offset][10-1] = firstdim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][22-1] = seconddim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][18-1] = thirddim

	
						if node == 6:

							base = self.src.variables["connect1"].getValue()[elem,node]
							firstdim = base + self.num_nodes() * (2 * offset + 0)
							secondim = base + self.num_nodes() * (2 * offset + 1)
							thirddim = base + self.num_nodes() * (2 * offset + 2)
							new_connect_data[elem + self.num_el_in_blk(1) * offset][11-1] = firstdim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][23-1] = seconddim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][19-1] = thirddim
				
						if node == 7:

							base = self.src.variables["connect1"].getValue()[elem,node]
							firstdim = base + self.num_nodes() * (2 * offset + 0)
							secondim = base + self.num_nodes() * (2 * offset + 1)
							thirddim = base + self.num_nodes() * (2 * offset + 2)
							new_connect_data[elem + self.num_el_in_blk(1) * offset][12-1] = firstdim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][24-1] = seconddim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][20-1] = thirddim
							
						if node == 8:

							base = self.src.variables["connect1"].getValue()[elem,node]
							firstdim = base + self.num_nodes() * (2 * offset + 0)
							secondim = base + self.num_nodes() * (2 * offset + 1)
							thirddim = base + self.num_nodes() * (2 * offset + 2)
							new_connect_data[elem + self.num_el_in_blk(1) * offset][25-1] = firstdim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][27-1] = seconddim
							new_connect_data[elem + self.num_el_in_blk(1) * offset][26-1] = thirddim

					else:
						if node == 0:
							firstdim = self.src.variables["connect1"].getValue()[elem,node]
							new_connect_data[elem][node] = firstdim 
							seconddim = firstdim + self.num_nodes()
							new_connect_data[elem + self.num_el_in_blk(1) * offset][13-1] = seconddim 
							thirddim = firstdim + self.num_nodes() * 2 
							new_connect_data[elem][5-1] = thirddim 
				
						if node == 1:
							firstdim = self.src.variables["connect1"].getValue()[elem,node]
							new_connect_data[elem][node] = firstdim 
							seconddim = firstdim + self.num_nodes()
							new_connect_data[elem][14-1] = seconddim 
							thirddim = firstdim + self.num_nodes() * 2
							new_connect_data[elem][6-1] = thirddim 
						
						if node == 2:
							firstdim = self.src.variables["connect1"].getValue()[elem,node]
							new_connect_data[elem][node] = firstdim 
							seconddim = firstdim + self.num_nodes()
							new_connect_data[elem][15-1] = seconddim 
							thirddim = firstdim + self.num_nodes() * 2
							new_connect_data[elem][7-1] = thirddim 
						
						if node == 3:
							firstdim = self.src.variables["connect1"].getValue()[elem,node]
							new_connect_data[elem][node] = firstdim 
							seconddim = firstdim + self.num_nodes()
							new_connect_data[elem][16-1] = seconddim 
							thirddim = firstdim + self.num_nodes() * 2
							new_connect_data[elem][8-1] = thirddim 
						if node == 4:
							firstdim = self.src.variables["connect1"].getValue()[elem,node]
							new_connect_data[elem][9-1] = firstdim 
							seconddim = firstdim + self.num_nodes()
							new_connect_data[elem][21-1] = seconddim 
							thirddim = firstdim + self.num_nodes() * 2
							new_connect_data[elem][17-1] = thirddim 

						if node == 5:
							firstdim = self.src.variables["connect1"].getValue()[elem,node]
							new_connect_data[elem][10-1] = firstdim 
							seconddim = firstdim + self.num_nodes()
							new_connect_data[elem][22-1] = seconddim 
							thirddim = firstdim + self.num_nodes() * 2
							new_connect_data[elem][18-1] = thirddim 
					
						if node == 6:
							firstdim = self.src.variables["connect1"].getValue()[elem,node]
							new_connect_data[elem][11-1] = firstdim 
							seconddim = firstdim + self.num_nodes()
							new_connect_data[elem][23-1] = seconddim 
							thirddim = firstdim + self.num_nodes() * 2
							new_connect_data[elem][19-1] = thirddim 
									
						if node == 7:
							firstdim = self.src.variables["connect1"].getValue()[elem,node]
							new_connect_data[elem][12-1] = firstdim 
							seconddim = firstdim + self.num_nodes() 
							new_connect_data[elem][24-1] = seconddim 
							thirddim = firstdim + self.num_nodes() * 2
							new_connect_data[elem][20-1] = thirddim 
						if node == 8:
							firstdim = self.src.variables["connect1"].getValue()[elem,node]
							new_connect_data[elem][25-1] = firstdim 
							seconddim = firstdim + self.num_nodes()
							new_connect_data[elem][27-1] = seconddim 
							thirddim = firstdim + self.num_nodes() * 2
							new_connect_data[elem][26-1] = thirddim 
		destination.createDimension('num_nodes', num_nodes)
		destination.createDimension('num_dim', 3)
		destination.createDimension('num_nod_per_el1', 27)
	        
		self.new_name_updated(destination,'name_nod_var',2,['DMZ','VZ'])
		num_nodes1 = self.num_nodes()
		max_nnv = self.num_nod_var()
		if exodus_results == 1:
			
			print "i am creating results"
			new_nodal_data = zeros((self.time_step(),self.num_nod_var() + 2,num_nodes), Float32)
			#for ts in range(0, self.time_step()):
			#	for nnv in range(0,self.num_nod_var()):
			#		for node in range(0,self.num_nodes()):
			#			for offset in range(0,new_eb):
			#				value = self.src.variables["vals_nod_var"][ts][nnv][node]
			#				new_nodal_data[ts][nnv][node + self.num_nodes() * offset] = value 
			for ts in range(0, self.time_step()):
				for node in range(0,self.num_nodes()):
					for offset in range(0,num_div):#new_eb):
						#print "next"
						xvalue = self.src.variables["vals_nod_var"][ts][0][node]
						yvalue = self.src.variables["vals_nod_var"][ts][1][node]
						r = sqrt(pow(xvalue,2) + pow(yvalue,2))
						#newx = r * cos(30 * offset * (pi/180)) 
						#newy = r * sin(30 * offset * (pi/180)) 
						#newz = xvalue
						#pdb.set_trace()
						new_nodal_data[ts][0][node + num_nodes1 * offset] = xvalue #newx
						new_nodal_data[ts][1][node + num_nodes1 * offset] = yvalue #newy
						new_nodal_data[ts][max_nnv][node + num_nodes1 * offset] = sqrt(pow(xvalue,2) + pow(yvalue,2)) #newy

			for ts in range(0, self.time_step()):
				for node in range(0,self.num_nodes()):
					for offset in range(0,num_div):#new_eb):
						xvalue = self.src.variables["vals_nod_var"][ts][2][node]
						yvalue = self.src.variables["vals_nod_var"][ts][3][node]
						r = sqrt(pow(xvalue,2) + pow(yvalue,2))
						newx = r * cos(30 * offset * (pi/180)) 
						newy = r * sin(30 * offset * (pi/180)) 
						newz = xvalue
						new_nodal_data[ts][2][node + self.num_nodes() * offset] = newx
						new_nodal_data[ts][3][node + self.num_nodes() * offset] = newy
						new_nodal_data[ts][self.num_nod_var() + 1][node + self.num_nodes() * offset] = sqrt(pow(xvalue,2) + pow(yvalue,2)) #newynewy

			for nnv in range(4,self.num_nod_var()):
				for ts in range(0, self.time_step()):
					for node in range(0,num_div):#self.num_nodes()):
						for offset in range(0,new_eb):
							value = self.src.variables["vals_nod_var"][ts][nnv][node]
							new_nodal_data[ts][nnv][node + self.num_nodes() * offset] = value
					#new_nodal_data[ts][self.num_nod_var() + 1][node + self.num_nodes() * offset] = newy
					#yvalue = self.src.variables["vals_nod_var"][ts][5][node]
					#r = sqrt(pow(xvalue,2) + pow(yvalue,2))
					#newx = r * cos(30 * offset * (pi/180)) 
					#newy = r * sin(30 * offset * (pi/180)) 
					#newz = xvalue
					#new_nodal_data[ts][][node + self.num_nodes() * offset] = yvalue
					#


			#new_nodal_data[ts][self.num_nod_var() + 2][node + self.num_nodes() * offset] = newy
			#destination.createDimension('num_nod_var', 14)
			nodal_dims = ('time_step', 'num_nod_var', 'num_nodes',)
			var = destination.createVariable('vals_nod_var','d',(nodal_dims))
			var.assignValue(new_nodal_data)
		

		#if exodus_results == 1:
		#	print "i am creating results"
		#	new_nodal_data = zeros((self.time_step(),self.num_nod_var(),num_nodes), Float32)
		#	for ts in range(0, self.time_step()):
		#		for nnv in range(0,self.num_nod_var()):
		#			for node in range(0,self.num_nodes()):
		#				for offset in range(0,new_eb):
		#					value = self.src.variables["vals_nod_var"][ts][nnv][node]
		#					new_nodal_data[ts][nnv][node + self.num_nodes() * offset] = value 


			#destination.createDimension('num_nod_var', 14)


			#nodal_dims = ('time_step', 'num_nod_var', 'num_nodes',)
			#var = destination.createVariable('vals_nod_var','d',(nodal_dims))
			#var.assignValue(new_nodal_data)
			
		else:
			pass
		

		
		######
		destination.createDimension('num_el_in_blk1', self.num_el_in_blk(1) * new_eb)
		destination.createDimension('num_elem', self.num_el_in_blk(1)* new_eb)

		connect_dim = ('num_el_in_blk1','num_nod_per_el1',)
		CONNECT1 = destination.createVariable('connect1','i',(connect_dim))
		CONNECT1.assignValue(new_connect_data)		
		setattr(CONNECT1,"elem_type","Hex")
		coord_dims = ('num_dim', 'num_nodes',)
		coord_data = list
		var = destination.createVariable('coord','d',(coord_dims))
		var.assignValue(new_coord_data)

		node_num_map_data = []
		for node in range(0, num_nodes):
			node = node + 1
			node_num_map_data.append(node)
		node_num_map_dim = ('num_nodes',)
		var = destination.createVariable("node_num_map",'i' ,node_num_map_dim)
		var.assignValue(node_num_map_data)

	def hex8(self,destination,array,delta,num_div = 2,side_set = 0):
		num_div = 30
		maxz = 3
		deltaz = 0
		num_nodes = self.num_nodes() * num_div
		new_coord_data = zeros((3, num_nodes), Float32)
		for node in range(0,self.num_nodes()):
			deltaz = 0
			for offset in range(0,num_div):
				x1 = self.src.variables["coord"].getValue()[0,node] 
				y1 = self.src.variables["coord"].getValue()[1,node]
				r = sqrt(pow(x1,2) + pow(y1,2))
				c = 20
				
				#xnew = x1*cos(rd)-sin(rd)*y1
				#ynew = cos(rd)*y1+x1*sin(rd)
				#znew = r * cos(rd)

				#xnew = x1
				#ynew = y1
				#znew = deltaz

				#matrix1 = [[

				#xnew = sqrt(pow(c,2) - pow(y1,2) - pow(deltaz,2))
				#ynew = sqrt(pow(c,2) - pow(x1,2) - pow(deltaz,2))
				#znew = sqrt(pow(c,2) - pow(y1,2) - pow(x1,2))

				new_coord_data[0][node + self.num_nodes() * offset] = xnew
				new_coord_data[1][node + self.num_nodes() * offset] = ynew
				new_coord_data[2][node + self.num_nodes() * offset] = znew
				deltaz = deltaz + 1
		list = []
		#new_connect_data =  zeros((self.num_el_in_blk(1),self.num_nod_per_el(1) * num_div), Int)
		new_connect_data =  zeros((num_div - 1,self.num_nod_per_el(1) * 2), Int)
		#print "the new coon shape is",new_connect_data.shape
		m_factor = 0
		for elem in range(0,num_div - 1):
			for node in range(0,self.num_nod_per_el(1)):
				firstdim = self.src.variables["connect1"].getValue()[0,node]
				seconddim = firstdim + self.num_nodes() #* offset
				new_connect_data[elem][node] = firstdim + m_factor 
				new_connect_data[elem][node + self.num_nod_per_el(1)] = seconddim + m_factor
			m_factor = m_factor + 4
			
		#print new_connect_data
		destination.createDimension('num_nodes', num_nodes)
		destination.createDimension('num_dim', 3)
		destination.createDimension('num_nod_per_el1', 8)
		destination.createDimension('num_el_in_blk1', num_div - 1)
		destination.createDimension('num_elem', num_div - 1)
		
		connect_dim = ('num_el_in_blk1','num_nod_per_el1',)
		CONNECT1 = destination.createVariable('connect1','i',(connect_dim))
		CONNECT1.assignValue(new_connect_data)		
		setattr(CONNECT1,"elem_type","Hex")
		coord_dims = ('num_dim', 'num_nodes',)
		coord_data = list
		var = destination.createVariable('coord','d',(coord_dims))
		var.assignValue(new_coord_data)
		node_num_map_data = []
		for node in range(0, num_nodes):
			node = node + 1
			node_num_map_data.append(node)
		node_num_map_dim = ('num_nodes',)
		var = destination.createVariable("node_num_map",'i' ,node_num_map_dim)
		var.assignValue(node_num_map_data)

	def new_name_updated(self,destination,variable,num_new_variables,new_names):
		length = self.num_nod_var() + num_new_variables
		destination.createDimension('num_nod_var',length)
		variable_names = []
		oldvar  = self.src.variables.get(variable)
		vartype= oldvar.typecode()
		dimension_names = ("num_nod_var","len_string")
		list = []
		nodal_var = self.name_nod_var()
		new_names = ['DMZ', 'VZ']
		name = ""
		variable_names = []
		for char in nodal_var:
			if len(char) < 33:
				for x in range(0,33-len(char)):
					char = char + '/0'

			#small_char = char.tostring()
			#print small_char
			#name += small_char
			variable_names.append(char)
		for newvarname in new_names:
			if len(newvarname) < 33:
				for x in range(0,33 - len(newvarname)):
					newvarname = newvarname + '\0'
					#newvarname.tostring()
					#print newvarname
					#print len(newvarname)
					#newvarname.append('\0')
			variable_names.append(newvarname)
		
		#print variable_names
		a = array(variable_names)
		print "shae",a.shape
		#a.astype(string)
		#new_name_nod_var = newvar.assignValue(a)

		#good_list = []
		#for x in range(0,14):
		 # #print x
		  #varname =  variable_name[x,:]
		  #var_as_string = varname.tostring()
		  #strip_string = str.rstrip(var_as_string)
		  #t=str.index(var_as_string, '\000')
		  #index = strip_string[:t]
		  #good_list.append(index)
		  #return good_list
		#new_shape = reshape(a,(self.num_nod_var(),33))
		newvar = destination.createVariable(variable,(vartype),(dimension_names))
		new_name_nod_var = newvar.assignValue(a)

	def typedefine(self,number):
		if isinstance(number, types.IntType) == 1:
			return "i"
		elif isinstance(number, types.FloatType) == 1:
			return "f"
		elif isinstance(number, types.LongType) == 1:
			return "l"
		elif isinstance(number, types.StringType) == 1:
			return "c"
		elif isinstance(number, types.CharType) == 1:
			return "c"
		elif isinstance(number, types.DoubleType) == 1:
			return "d"
		else:
			print "need to add support for",type(number)
	
	def extrude2(self,destination, destination2,  num_divisions, array, delta, side_set = 0):
		self.connectivity_data = []
		self.coordinate_data = []
		self.number_nodes = 0
		self.number_element_blocks = 0
		self.nodal_map = []
		xlist = []
		ylist = []
		zlist = []
		array = self.coord()
		num_nodes = len(array[1])
		list = array.tolist()
		xlist = list[0]
		ylist = list[1]
		connect1_data = []
		connectlist = []
		num_dim = self.num_dim() + 1
		num_nodes = self.num_nodes() * 2
		new_coord_data = zeros((num_dim, num_nodes), Float32)
		#for node in range(0,1):
		destination.createDimension('time_step', self.time_step())
		########################################################
		e.copy_dimensions_for_slice(destination,[
			                                 'num_node_sets',
							 'num_elem',
							 'num_el_in_blk1',
							 'num_df_ss2',
							 'num_side_sets',
							 'num_df_ss3',
							 'num_glo_var',
							 'num_df_ss1',
							 'num_nod_var',
							 'num_nod_ns2',
							 'num_nod_ns1',
							 'num_nod_ns5',
							 'num_nod_ns4',
							 'num_side_ss1',
							 'num_side_ss3',
							 'num_side_ss2',
							 'num_nod_ns3',
							 'num_nodes',
							 'num_dim',
							 'num_nod_per_el1',
							 'num_df_ss2',
							 'num_df_ss3',
							 'num_nod_var',
							 'num_df_ss1',
							 'num_glo_var',
							 'num_nod_ns2',
							 'num_nod_ns1',
							 'num_nod_ns5',
							 'num_nod_ns4',
							 'num_side_ss1',
							 'num_side_ss3',
							 'num_side_ss2',
							 'num_nod_ns3'
							 'num_node_sets',
							 'num_df_ss2',
							 'num_side_sets',
							 'num_df_ss3',
							 'num_df_ss1',
							 'time_step',
							 'node_num_map',
							 
							 ])

	#	self.hex8(destination,destination2, 1, 5)
		self.hex27(destination,destination2, 1, 1)
		self.new_var_vars(destination,['num_df_ss2',
					       'name_nod_var',
					       'side_ss3',
					       'side_ss1',
					       'vals_glo_var',
					       'dist_fact_ss3',
					       'dist_fact_ss2',
					       'dist_fact_ss1',
					       'ns_status',
					       'node_ns1',
					       'ss_prop1',
					       'dist_fact_ns1',
					       'name_glo_var',
					       'node_ns2',
					       'node_ns3',
					       'dist_fact_ns4',
					       'dist_fact_ns5',
					       'dist_fact_ns2',
					       'dist_fact_ns3',
					       'node_ns4',
					       'node_ns5',
					       'elem_ss2',
					       'elem_ss3',
					       'elem_ss1',
					       'ns_prop1',
					       'ss_status',
					       'coord',
					       'coor_names',
					       'connect1',
					       'vals_nod_var',
					       'node_num_map'
					       'ns_status',
					       'ns_prop1',
					       'ss_status',
					       'ss_prop1',
					       'node_ns1',
					       'dist_fact_ns1',
					       'node_ns2',
					       'dist_fact_ns2',
					       'int node_ns3',
					       'dist_fact_ns3',
					       'node_ns4',
					       'dist_fact_ns4',
					       'node_ns5',
					       'dist_fact_ns5',
					       'elem_ss1',
					       'side_ss1',
					       'dist_fact_ss1',
					       'elem_ss2',
					       'side_ss2',
					       'dist_fact_ss2',
					       'elem_ss3',
					       'side_ss3',
					       'node_num_map',
					       'name_nod_var'
					       ])
		
		
		coor_names_dims = ('num_dim', 'len_string',)
		coor_names_data = ['x',
				   'y',
				   'z                                ']
		var = destination.createVariable('coor_names',self.typedefine(coor_names_data[1]),(coor_names_dims))
		var.assignValue(coor_names_data)
		api = zeros((1,), Float32)
		api[0] = 4.01000023
		ver = zeros((1,), Float32)
		ver[0] = 3.00999999
		atts = {
			'api_version' : api ,
			'version' : ver,
			'floating_point_word_size' :  [8],
			'file_size' : [0] ,
			'title' : "One element box" 
			}
		for att, value in atts.iteritems():
			setattr(destination,att,value)
		#self.addanotherdim(num_nodes,2,10)
		destination.close()

        def create_Sideset(self,block,sideset_number,destination):
          """
          Need to work with
          Num_Side_Sets
          """
	  numsidess = "num_side_ss"+ repr(self.num_side_sets() + 1)
	  numdfss = "num_df_ss" + repr(self.num_side_sets() + 1)
	  numsidesets = self.num_side_sets() + 1
	  elemss = "elem_ss" + repr(self.num_side_sets() + 1) 
	  sidess = "side_ss" + repr(self.num_side_sets() + 1)
	  distfactss = "dist_fact_ss" + repr(self.num_side_sets() + 1)
	  exception_list3 = [numsidess, numdfss]
	  exception_list2 = ["num_side_ss1", "num_df_ss1"]
	  length = self.dimensions["num_side_sets"]
	  destination.createDimension("num_side_sets", length + 1)

	  try:
		  for d in self.dimensions.keys():
			  if d in exception_list2:
				  length = self.src.dimensions[d]
				  destination.createDimension(d,length)
				  print "just created", d
	  except IOError,e:
		  pass
	  for l in range(0,len(exception_list3)):
		  length = self.src.dimensions[exception_list2[l]]
		  destination.createDimension(exception_list3[l],length)
		  print "just created", exception_list3[l]
	  exception_list4 = ["ss_prop1", elemss, sidess, distfactss]
	  exception_list = ["ss_prop1", "elem_ss1","side_ss1", "dist_fact_ss1"]
	  for var in range(0,len(exception_list)):
		    if exception_list[var] == "ss_prop1":
			    getvars = self.src.variables[exception_list[var]]
			    vardata = getvars.getValue()
			    thisvar= self.src.variables[exception_list[var]]
			    vartype  = thisvar.typecode()
			    self.num_el_in_blk = self.src.dimensions[num_el_in_blk]
			    var1 = destination.createVariable(exception_list[var],(vartype) ,(thisvar.dimensions))
			    list = self.ss_prop(1)
			    list2 = []
			    for x in range(0,len(list)):
				    list2.append(list[x])
			    list2.append(sideset_number)
			    w = array(list2)
			    self.ss_prop(1,w)
			    destination.sync()
			    var1.assignValue(list2)
			    x = self.src.variables[exception_list[var]]
		    else:
			    print "On var",exception_list[var]
			    getvars = self.src.variables[exception_list[var]]
			    vardata = getvars.getValue()
			    thisvar= self.src.variables[exception_list[var]]
			    vartype  = thisvar.typecode()
			    var1 = destination.createVariable(exception_list4[var],(vartype) ,(thisvar.dimensions))
			    var1.assignValue(vardata)
	  destination.sync()
        
        def createexofile(self):
            pass



        def dimension_check(self,varnname):
            coord = ['num_dim','num_nodes']
            coor_names = ['num_dim','len_string']
            connect = ['num_el_in_blk', 'num_nod_per_el']
            attrib = ['num_el_in_blk', 'num_att_in_blk']
            eb_prop = ['num_elem']
            elem_map = ['num_elem']
            dist_fact_ss = ['num_df_ss']
            elem_ss = ['num_side_ss']
            side_ss = ['num_side_ss']
            ss_prop = ['num_side_sets']
            node_ns = ['num_nod_ns']
            dist_fact_ns = ['num_nod_ns']
            ns_prop = ['num_node_sets']
            qa_records = ['num_qa_rec',4,'len_string']
            info_records = ['num_info', 'len_line']
            time_whole = ['time_step']
            elem_var_tab = ['num_el_blk', 'num_elem_var']
            name_glo_var = ['num_glo_var', 'len_string']
            vals_glo_var = ['time_step', 'num_glo_var']
            name_nod_var = ['num_nod_var', 'len_string']
            vals_nod_var = ['time_step', 'num_nod_var', 'num_nodes']
            name_elem_var = ['num_elem_var', 'len_string']
            vals_elem_var = ['time_step', 'num_el_in_blk']
            allObs = { 'coord' : coord,
                       'coor_names' : coor_names, 
                       'connect' : connect,
                       'attrib' : attrib,
                       'eb_prop' : eb_prop,
                       'elem_map' : elem_map,
                       'dist_fact_ss' : dist_fact_ss,
                       'elem_ss' : elem_ss,
                       'side_ss' : side_ss,
                       'ss_prop' : ss_prop,
                       'node_ns' : node_ns,
                       'dist_fact_ns' : dist_fact_ns,
                       'ns_prop' : ns_prop,
                       'qa_records' : qa_records,
                       'info_records' : info_records,
                       'time_whole' : time_whole,
                       'elem_var_tab' : elem_var_tab,
                       'name_glo_var' : name_glo_var,
                       'vals_glo_var' : vals_glo_var,
                       'name_nod_var' : name_nod_var,
                       'vals_nod_var' : vals_nod_var,
                       'name_elem_var' : name_elem_var,
                       'vals_elem_var' : vals_elem_var
                       }
            return allObs[varnname]
            #print allObs.keys()
        def variable_name_formatter(self,varname,number):
            pass

        def dependency_check(self,varname):
            #note missing a lot of variables
            num_nodes = ['coord','vals_nod_var']
            num_dim = ['coord','coor_names']
            num_elem = ['elem_map']
            num_el_blk = ['eb_prop']
            num_el_in_blk_x = ['connect']
            num_nod_per_el_x = ['connect']
            num_att_in_blk_x = []
            num_side_sets = ['ss_prop']
            num_side_ss_x = ['elem_ss','side_ss']
            num_df_ss_x = ['dist_fact_ss']
            num_node_sets = ['ns_prop']
            num_nod_ns_x = ['node_ns','node_ns']
            num_df_ns_x = []
            num_qa_rec = []
            num_info = []
            num_glo_var = ["name_glo_var",'vals_glo_var']
            num_nod_var = ['name_nod_var']
            num_elem_var = []
            time_step = ['time_whole','vals_glo_var','vals_nod_var']
            len_string = []
            four = []
            

            allObs = {'num_nodes' : num_nodes,
                      'num_dim': num_dim,
                      'num_elem': num_elem,                
                      'num_el_blk': num_el_blk, 
                      'num_el_in_blk_x':  num_el_in_blk_x,
                      'num_nod_per_el_x': num_nod_per_el_x,
                      'num_att_in_blk_x': num_att_in_blk_x,
                      'num_side_sets': num_side_sets,
                      'num_side_ss_x': num_side_ss_x,
                      'num_df_ss_x': num_df_ss_x,
                      'num_node_sets': num_node_sets,
                      'num_nod_ns_x': num_nod_ns_x,
                      'num_df_ns_x': num_df_ns_x,
                      'num_qa_rec': num_qa_rec,
                      'num_info': num_info,
                      'num_glo_var': num_glo_var,
                      'num_nod_var': num_nod_var,
                      'num_elem_var': num_elem_var,
                      'time_step':  time_step,
                      'len_string': len_string,
                      'four': four
                      }
            #return allObs[varname]#[x]
            #print allObs.keys()
            #print len(allObs['num_nodes'])
            #for x in range(0,len(allObs['num_nodes'])):
            #    print allObs['num_nodes'][x]
        def is_var(self,varname):
            try:
                self.src.variables[varname]
                return 1
            except KeyError,e:
                print "the var needs to be added"
                return 0
            
        def is_dim(self,dimname):
            try:
                self.src.dimensions[dimname]
                return 1
            except KeyError,e:
                return 0
        
        def test_validity(self):
            print "is var",e.is_var('vals_elem_var')

            print "is dim",e.is_dim('num_glo_var')
            print self.src.variables['time_whole'].dimensions
            print self.dependency_check('time_whole')
                #print var,(vartype) ,(getvars.dimensions))
            
        def create_new_dim(self,dimname,destination):
            if self.is_dim(dimname) == 0:
                self.whole_new_dim(dimname)
            else:
                self.new_var_dims(destination,[dimname])
                if dimname == 'num_nodes':
                    pass
                if dimname == 'num_dim':
                    pass
                if dimname == 'num_elem':
                    pass

                if dimname == 'num_el_blk':    
                    pass

                if dimname == 'num_side_sets':
                    pass

                if dimname == 'num_node_sets':
                    pass
                    
                if dimname == 'time_step':
                    pass

                if dimname == 'num_qa_rec':
                    pass

                if dimname == 'num_info':
                    pass
                
                if dimname == 'num_glo_var':
                    pass

                if dimname == 'num_nod_var':
                    pass
                
                if dimname == 'num_elem_var':
                    pass
                else:
                    pass
        def create_new_var(self,varname,destination):
            if self.is_dim(dimname) == 0:
                self.whole_new_var(varname)
            else:
                new_var_vars(destination,[varname])
                if varname == 'vals_nod_var':
                    pass
                if varname == 'vals_elem_var':
                    pass
                if varname == 'vals_glo_var':
                    pass
                if varname == 'side_set':
                    pass
                if varname == 'node_set':
                    pass
                if varname == 'elem_blk':
                    pass
        def whole_new_var(self,destination,varname,vardata):
            '''
            This function creates a variable that has never been
            in the exodus file before
            '''
            print destination.dimension_check('time_whole')
            if varname == 'time_whole':
                for x in range(len(e.dimension_check('time_whole'))):
                    #print destination.dimension_check('time_whole')[x]
                    if e.is_dim(destination.dimension_check('time_whole')[x]) == 0:
                        print "i am in here"
                        self.whole.new_dim(e.dimension_check('time_whole')[x])
                    else:
                        pass
                
                destination.createVariable(varname,self.typedefine(vardata[1]) ,tuple(e.dimension_check('time_whole')))                

        def whole_new_dim(self,dimname):
            print "will implement soon"

        def get_current_data(self):
            pass
