Installing mrsimform
====================

Getting mrsimform running the first time can be très-annoying!  On ubuntu, with
CDH3, it's actually pretty painless.  But no one who puts up real clusters
seems to use Ubuntu.  

Requirements:
* A recent branch of python2, say 2.6
* [dumbo](https://github.com/klbostee/dumbo)
* [dumbo-feathers](https://github.com/klbostee/feathers) -- this requires compiling some Java against the
  current version of Hadoop  
* A version of the JDK to compile dumbo-feathers  
* numpy
* pynetcdf or scipy with netcdf (Scientific.IO.NetCDF)
* make -- nothing special here, any version should do
* Hadoop -- tested with CDH3, earlier prototypes tested with Hadoop 0.21
* [mrtsqr](https://github.com/arbenson/mrtsqr) -- 

Recommended:
* [ctypedbytes](https://github.com/klbostee/ctypedbytes) -- this makes
all the IO go faster



