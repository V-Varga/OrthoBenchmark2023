#!/bin/python
# -*- coding: utf-8 -*-
"""

Title: create_ortho_db.py
Date: 2023.10.26
Author: Vi Varga

Description:
	This program parses the *_parsed_pivot.txt output file of the ortho_results_parser.py 
		program, in order to create or modify a large database associating query protein 
		IDs with their assigned orthologous clusters. 

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	datetime.datetime
	pandas

Procedure:
	1. Loading required modules & assigning command line arguments.
	2. Load dataframe into Pandas
	3. Merge dataframes into larger ortholog database
	4. Print results to tab-separated text file 

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file names are not user-defined, but are instead based on the 
		program command line submission time. 

Usage
	./create_ortho_db.py input_db1 [input_db2 input_db3...]
	OR
	python create_ortho_db.py input_db1 [input_db2 input_db3...]
	
	Where the input_db should be either a *_parsed_pivot.txt file output by the 
		ortho_results_parser.py program, or an orthology database previously generated
		by this program (Orthology_Comparison_DB__*.txt).

This script was written for Python 3.9.18, in Spyder 5.4.3. 

"""


# Part 1: Import modules & assign command line arguments

# import necessary modules
import sys # allows execution of script from command line
import os # allow access to computer files
from datetime import datetime # access data from system regarding date & time
import pandas as pd # allows manipulation of dataframes


# determine input files

# create empty list to contain command line arguments
db_args = []

for idx, x in enumerate(sys.argv[1:]):
	# loop over the command line arguments
	# ref:https://stackoverflow.com/questions/34791923/loop-over-sys-args
	# ref: https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops
	# get the index to use for each argument
	arg_idx = idx + 1
	looping_db_arg = sys.argv[arg_idx]
	# add the argument to the list
	db_args.append(looping_db_arg)


# designate output file name
# first determine date & time of query
now = datetime.now()
time_now = now.strftime("%d-%m-%Y--%H%M%S")
#and create the resulting outfile name
output_db = "Orthology_Comparison_DB__" + time_now + ".txt"


# Part 2: Build the query-based orthology database

if len(db_args) == 1: 
	# check to see if only 1 argument is given
	# in which case, simply parse & flip the single database
	input_db = db_args[0]
	# determine the basename of the input file
	# this will also be used in the OG column name
	base = os.path.basename(input_db)
	out_base = os.path.splitext(base)[0]
	# import the dataframe into Pandas
	input_df = pd.read_csv(input_db, sep='\t', header=0, low_memory=False)
	# switch the column order
	# ref: https://stackoverflow.com/questions/13148429/how-to-change-the-order-of-dataframe-columns
	cols = input_df.columns.tolist()
	cols = cols[-1:] + cols[:-1]
	input_df = input_df[cols]
	# rename the columns
	# ref: https://stackoverflow.com/questions/11346283/renaming-column-names-in-pandas
	input_df.columns = ['Query', out_base]
	# and write out the results to a tab-separated text file
	input_df.to_csv(output_db, index=False, header=True, sep = '\t')


else: 
	# if there is >1 element in the list of input files
	for db_idx, i in enumerate(db_args): 
		# loop over the elements of the input dataframe list
		# save the specific database as a variable
		input_db = db_args[db_idx]
		# import the dataframe into Pandas
		input_df = pd.read_csv(input_db, sep='\t', header=0, low_memory=False)
		if db_idx == 0: 
			# for the first element in the list of input dataframes
			# check if the input is already in the style of the large orthology dataframe
			if input_df.columns[0] != "Query": 
				# if the dataframe is not already formatted in the large dataframe style
				# determine the basename of the input file
				# this will also be used in the OG column name
				base = os.path.basename(input_db)
				out_base = os.path.splitext(base)[0]
				# switch the column order
				cols = input_df.columns.tolist()
				cols = cols[-1:] + cols[:-1]
				input_df = input_df[cols]
				# rename the columns
				input_df.columns = ['Query', out_base]
				# then copy the contents of this dataframe into what will be the large dataframe
				ortho_df = input_df.copy()
			else: 
				# if the input database is already in the format of the large database
				# simply copy the dataframe into the larger dataframe name
				ortho_df = input_df.copy()
		else: 
			# for all other elements of the list of dataframes
			# determine the basename of the input file
			# this will also be used in the OG column name
			base = os.path.basename(input_db)
			out_base = os.path.splitext(base)[0]
			# switch the column order
			cols = input_df.columns.tolist()
			cols = cols[-1:] + cols[:-1]
			input_df = input_df[cols]
			# rename the columns
			input_df.columns = ['Query', out_base]
			# join the contents of the input dataframe into the larger dataframe
			# ref: https://stackoverflow.com/questions/53645882/pandas-merging-101
			# ref: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html
			ortho_df = ortho_df.merge(input_df, on='Query', how='outer').fillna('-')
	# finally, write out the large OG dataframe to a tab-separated text file
	ortho_df.to_csv(output_db, index=False, header=True, sep = '\t')
