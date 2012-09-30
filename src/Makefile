# This Makefile is to create a new Makefile with all the info for automated run.
#
# History
# -------
# :2012-09-14: initial coding
#
# Example Usage:
# make setup_database name=runs variable=TEMP \
#      dir=hdfs://icme-hadoop1.localdomain/user/yangyang/simform/ \
# 	   outdir=hdfs://icme-hadoop1.localdomain/user/yangyang/simform/output
#
# Author = 'Yangyang Hou <hou13@purdue.edu>'

name?=
dir?=
variable?=
outdir?=$(dir)output/

setup_database: 
	@echo '========================================';\
	echo 'Setting up the database...';\
	python setup_database.py $(name) $(dir) $(variable) $(outdir);\
	echo 'Set up done! The new makefile "$(name)" is generated.'

.PHONY: clean 	
clean:
	@rm $(name); echo 'The makefile "$(name)" removed!'