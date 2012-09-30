"""
This is a script to create a new makefile with all the info for runs in it.

Example usage:
    python setup_database.py runs hdfs://icme-hadoop1.localdomain/user/yangyang/simform/ TEMP
           
Yangyang Hou  hou13@purdue.edu
Copyright (c) 2012
"""

__author__ = 'Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os

name = sys.argv[1]
dir = sys.argv[2]
variable = sys.argv[3]
outdir = sys.argv[4]

if not dir.endswith('/'):
    dir  = dir + '/'
    
if not outdir.endswith('/'):
    outdir  = outdir + '/'
    
makefile = open(os.path.join('./', name),'w')

Header="# This is a makefile script to run scripts automatically\n"+\
"#\n"+\
"# Example usage:\n"+\
"#     make -f "+name+" convert # convert exodus files to sequence files\n"+\
"#     make -f "+name+" model # compute the SVD\n"+\
"#     make -f "+name+" predict design=<design sites> points=<interpolation sites>\n"+\
"#     make -f "+name+" check # make sure the database is \"correct\"\n"+\
"#\n"+\
"# Yangyang Hou  hou13@purdue.edu\n"+\
"# Copyright (c) 2012\n\n"

Variables="dir?="+dir+"\n"+\
"variable?="+variable+"\n"+\
"outdir?="+outdir+\
"""

SVD?=False

timesteps?=10
tmpdir?=./
timestepfile?=none
numExodusfiles?=

inputfile=$(outdir)input.txt
exodus2seq_output?=$(outdir)data.seq/

mseq_input=$(exodus2seq_output)*/*part*.seq
mseq_output?=$(outdir)data.mseq/

model_input?=$(mseq_output)
model_output?=$(outdir)model

predict_input=$(exodus2seq_output)*/*part*.seq
predict_output?=$(outdir)predict/noSVD/
design?=
points?=


predict_SVD_input?=$(model_output)_4/
predict_SVD_output?=$(outdir)predict/SVD/
weights?=

seq2exodus_input?=$(predict_output)part*
seq2exodus_output?=$(outdir)interpexodus/noSVD/

seq2exodus_SVD_input?=$(predict_SVD_output)part*
seqexodus_SVD_output?=$(outdir)interpexodus/SVD/
output_name?=

"""

Preprocess="""
preprocess: preprocess.py grabtemplate.py
	@echo '========================================';\\
	echo 'Preprocessing...';\\
	python preprocess.py $(dir) $(exodus2seq_output) $(variable) $(inputfile);\\
	echo 'Preprocess Done!'; \\
	echo '========================================'
"""

Convert="""
simform-deploy.tar.gz: exopy2.py exopy.py
	tar czf simform-deploy.tar.gz exopy2.py
	
convert: mr_exodus2seq_hadoop.py simform-deploy.tar.gz
ifeq ($(timestepfile),none)
	@echo '========================================';\\
	echo 'Converting exodus files to sequence files...';\\
	hadoop fs -test -z $(inputfile) || time python mr_exodus2seq_hadoop.py \\
	$(inputfile) -r hadoop --python-archive simform-deploy.tar.gz \\
	-t $(timesteps) -d $(exodus2seq_output) --variables $(variable) --no-output; \\
	echo 'Convert exodus files to sequence files Done!'; \\
	echo '========================================'
else
	@echo '========================================';\\
	echo 'Converting exodus files to sequence files using normalized timesteps...';\\
	test -e $(timestepfile) || echo 'The timestepfile does not exist!'; \\
	test -e $(timestepfile) && hadoop fs -test -z $(inputfile) \\
	|| time python mr_exodus2seq_hadoop.py \\
	$(inputfile) -r hadoop --python-archive simform-deploy.tar.gz --no-output \\
	-t $(timesteps) -d $(exodus2seq_output) --variables $(variable) \\
	--timestepfile $(timestepfile)  --file $(timestepfile) && \\
	echo 'Convert exodus files to sequence files using normalized timesteps Done!'; \\
	echo '========================================'
endif
	
"""

Seq2Mseq="""
seq2mseq:mr_seq2mseq_hadoop.py
	@echo '========================================';\\
	echo 'Converting sequence files to matrix sequence files...'; \\
	hadoop fs -test -e $(mseq_output) && \\
	python check_time.py $(exodus2seq_output) $(mseq_output) && \\
	hadoop fs -rmr $(mseq_output);\\
	hadoop fs -test -e $(mseq_output) || \\
	time python mr_seq2mseq_hadoop.py $(mseq_input) -r hadoop \\
	--no-output -o $(mseq_output) --variable $(variable); \\
	echo 'Convert to matrix sequence files Done!';\\
	echo '========================================'
	
"""


Model="""
.PHONY: model
model:
	@echo '========================================';\\
	echo 'SVD Modeling...';\\
	cd model; \\
	python run_full_tsqr.py --input=$(model_input) \\
	--ncols=$(numExodusfiles) --svd=2 --schedule=100,100,100 \\
	--hadoop=/usr/lib/hadoop --local_output=tsqr-tmp \\
	--output=$(model_output); \\
	cd ..; \\
	echo 'SVD Model Done!';\\
	echo '========================================'

"""

Weights="""
# create weights.txt file for predicting with SVD
"""


Predict="""
predict:mr_predict_hadoop.py mr_predictwithSVD_hadoop.py 
ifeq ($(SVD),False)
	@echo '========================================';\\
	echo 'Predicting directly using existing exodus files database...';\\
	test -e $(design) || echo 'The design sites file does not exist!'; \\
	test -e $(points) || echo 'The interpolation sites file does not exist!'; \\
	test -e $(design) && test -e $(points) && \\
	hadoop fs -test -e $(predict_output) && \\
	python check_time.py $(exodus2seq_output) $(predict_output) && \\
	hadoop fs -rmr $(predict_output) && \\
	time python mr_predict_hadoop.py $(predict_input) -r hadoop --no-output \\
	-o $(predict_output) --variable $(variable) \\
	--design=$(design) --points=$(points) --file $(design) --file $(points); \\
	echo 'Prediction Done!'; \\
	echo '========================================' 
else
ifeq ($(SVD),True)
	@echo '========================================';\\
	echo 'Predicting with SVD model...';\\
	test -e $(weights) || echo 'The weights file does not exist!'; \\
	test -e $(weights) && \\
	hadoop fs -test -e $(predict_SVD_output) && \\
	python check_time.py $(predict_SVD_input) $(predict_SVD_output) && \\
	hadoop fs -rmr $(predict_SVD_output) && \\
	time python mr_predictwithSVD_hadoop.py $(predict_SVD_input) -r hadoop --no-output \\
	-o $(predict_SVD_output) --variable $(variable) \\
	--weights=$(weights)  --file $(weighs); \\
	echo 'Prediction Done!'; \\
	echo '========================================' 
end
end
"""

Seq2Exodus="""
seq2exodus: mr_outputexodus_hadoop.py mr_outputexoduswithSVD_hadoop.py
ifeq ($(SVD),False)
	@echo '========================================' && \\
	echo 'Converting interpolated sequence files to interpolated exodus files...' && \\
	time python mr_outputexodus_hadoop.py $(seq2exodus_input) --outputname $(output_name) \\
	--variable $(variable)  --outdir $(seq2exodus_output) --indir $(dir)\\
	&& echo 'Convert to new interpolated exodus files Done!' && \\
	echo '========================================'
else
ifeq ($(SVD),True)
	@echo '========================================' && \\
	echo 'Converting interpolated sequence files to interpolated exodus files with SVD...' && \\
	time python mr_outputexoduswithSVD_hadoop.py $(seq2exodus_SVD_input) --outputname $(output_name) \\
	--variable $(variable)  --outdir $(seq2exodus_SVD_output) --indir $(dir)\\
	&& echo 'Convert to new interpolated exodus files Done!' && \\
	echo '========================================'
end
end
"""
	
Check="""
check:
"""

Clean="""
.PHONY: clean 
clean:
	@echo '========================================';\\
	echo 'Removing temporary files in local and on HDFS...';\\
	test -e $(tmpdir)tmp && rm -r $(tmpdir)tmp;\\
	hadoop fs -rm $(inputfile);\\
	echo 'Clean Done!'; \\
	echo '========================================'
"""

makefile.write(Header)
makefile.write(Variables)
makefile.write(Preprocess)
makefile.write(Convert)
makefile.write(Seq2Mseq)
makefile.write(Model)
makefile.write(Weights)
makefile.write(Predict)
makefile.write(Seq2Exodus)
makefile.write(Check)
makefile.write(Clean)

makefile.close()