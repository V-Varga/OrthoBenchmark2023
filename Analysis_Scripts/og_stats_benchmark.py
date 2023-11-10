# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: og_stats_benchmark.py
Date: 2023.10.27
Author: Vi Varga

Description:
	This program performs basic descriptive statistical tests on orthologous clusters
		previously parsed into JSON dictionaries via the ortho_results_parser.py
		script.

List of functions:
	No functions are used in this script.

List of standard and non-standard modules used:
	sys
	datetime.datetime
	pandas
	os
	json
	statistics

Procedure:
	1. Importing modules & assigning command-line arguments. 
	2. Creating empty dataframe with Pandas to contain statistics.
	3. Calculating & compiling statistics: source file, number of clusters, minimum 
		cluster size, maximum cluster size, average/mean cluster size, median cluster 
		size, mode cluster size, standard deviation of cluster sizes, variance in 
		size, presence of single-protein OGs. 
	4. Writing out results to text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The basename of the output file can be, optionally, user-defined.
	- This program is designed only to accept JSON dictionary input files created
		by the ortho_results_parser.py script. 

Version: 
	This is version 3.0 of this program. The earlier published version (og_stats__v2.py) 
		can be found in the following GitHub repository: 
			https://github.com/V-Varga/TrichoCompare/tree/main
	This version of the program has been streamlined and adapted to the parsed results 
		of different orthologous clustering programs and a new project. 

Usage:
	./og_stats_benchmark.py input_dict [input_dict2 input_dict3 ...] [-NAME out_base]
	OR
	python og_stats_benchmark.py input_dict [input_dict2 input_dict3 ...] [-NAME out_base]
	
	Where any number of input JSON dictionaries produced by the ortho_results_parser.py 
		script can be accepted as input. This program will compute descriptive statistics
		on all programs, and compile the data into a large output database. 
	Where the basename of the output database can be determined by the user if, after 
		listing the input JSON dictionary files on the command line, the user writes
		-NAME out_base (where out_base is the user-defined basename).

This script was written for Python 3.9.18, in Spyder 5.4.3. 

"""

# Part 1: Import necessary modules & assign command-line arguments

# import necessary modules
import sys # allows execution of script from command line
from datetime import datetime # access data from system regarding date & time
import json # allows import and export of data in JSON format
import pandas as pd # allows manipulation of dataframes in Python
import os # allows access to the file system
import statistics # allows calculation of statistics in Python


# assign command line arguments

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

# set up output file name
if (len(db_args) >= 3 and db_args[-2] == "-NAME"): 
	# if the user has designated an output file basename
	out_base = sys.argv[-1]
	# designate the outfile name
	output_db = out_base + "__og_stats.txt"
	# then remove these elements from the input dictionary list
	# ref: https://www.geeksforgeeks.org/python-remove-last-k-elements-of-list/
	db_args = db_args[: len(db_args) - 2]
else: 
	# if the user has not desiganted an outfile basename
	# designate an automoatic output file name
	# first determine date & time of query
	now = datetime.now()
	time_now = now.strftime("%d-%m-%Y--%H%M%S")
	#and create the resulting outfile name
	output_db = "Orthology_Comparison_Stats__" + time_now + ".txt"


# Part 2: Set up output Pandas dataframe

# create empty dataframe to contain statistics
# ref: https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-and-then-filling-it
col_names =  ['OG_Source', 'Cluster_Num', 'Min_Size', 'Max_Size', 'Avg_Mean_Size', 
			  'Median_Size', 'Mode_Size', 'Std_Dev', 'Variance', 'Singletons', 'Singleton_Num']
stats_df = pd.DataFrame(columns = col_names)


# Part 3: Calculate OG statistics

for db_idx, i in enumerate(db_args): 
	# loop over the elements of the input dictionary list
	# save the specific dictionary as a variable
	input_db = db_args[db_idx]
	# import the JSON file into a Python dictionary
	# ref: https://www.geeksforgeeks.org/convert-json-to-dictionary-in-python/
	with open(input_db, "r") as json_file:
		# open the JSON file for reading
		# and extract its contents to a dictionary
		og_dict = json.load(json_file)
	# create empty list to populate with information on OG sizes
	size_list = []
	for key in og_dict.keys(): 
		# loop over the elements in the dictionary to extract size information
		length_og = len(og_dict[key])
		# save the length of each list of proteins (per OG) to variable length_og
		# and append this value to the size list
		size_list.append(length_og)
	# from here, compile the basic statistics into variables in a list
	
	# identifying the OG source file
	# then use the input file basename
	base = os.path.basename(input_db)
	out_base = os.path.splitext(base)[0]
	# assume that the input file comes from ortho_results_parser.py
	# and cut off the "_parsed" at the end of the base file name
	out_base = out_base.replace("_parsed", "")
	
	# Number of clusters
	clust_num = len(og_dict)
	
	# Minimum cluster size
	min_size = min(size_list)
	
	# Maximum cluster size
	max_size = max(size_list)
	
	# Avg/Mean cluster size
	mean_size = statistics.mean(size_list)
	
	# Median cluster size
	median_size = statistics.median(size_list)
	
	# Mode cluster size
	mode_size = statistics.mode(size_list)
	
	# Standard Deviation of size distribution
	# ref: https://www.geeksforgeeks.org/python-standard-deviation-of-list/
	std_dev_size = statistics.pstdev(size_list)
	
	# Variance of size distribution
	variance_size = statistics.pvariance(size_list)
	
	# Are there singletons? 
	# ref: https://www.geeksforgeeks.org/check-if-element-exists-in-list-in-python/
	if 1 in size_list: 
		# see if the value 1 is in the list
		singleton_yn = "Y"
	else: 
		# if there are no singletons
		singleton_yn = "N"
	
	# Number of singletons
	singleton_num = size_list.count(1)
	
	# compile the aboe information into a list
	clust_type_list = [out_base, clust_num, min_size, max_size, mean_size, median_size, 
					mode_size, std_dev_size, variance_size, singleton_yn, singleton_num]
	# and add the list content as a row to the larger dataframe
	# ref: https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-and-then-filling-it
	stats_df.loc[len(stats_df)] = clust_type_list


# Part 4: Write out results

# write out results to a tab-separated text file
stats_df.to_csv(output_db, index=False, header=True, sep = '\t')
