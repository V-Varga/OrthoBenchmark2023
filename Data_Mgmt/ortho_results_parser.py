#!/bin/python
# -*- coding: utf-8 -*-
"""

Title: ortho_results_parser.py
Date: 2023.10.25
Author: Virág Varga

Description:
	This program takes an input results file from an orthologous clustering software,
		and performs pre-determined data restructuring and extraction processes on the file.
	Three results files will be produced: a JSON dictionary, an expanded pivot table, 
		and a compressed comma-separated pivot table.
	The prediction software whose results files can be used as input are:
		- CD-HIT
		- Diamond
		- MMseqs2
		- USEARCH

List of functions:
	No functions are used in this script.

List of standard and non-standard modules used:
	argparse
	os
    pandas
	re
	json

Procedure:
	1. Assignment of command-line arguments.
	2. Importing of modules
	3. Designation of input and output files
	4. Parsing input file and outputting results

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The basename of the output file can optionally be user-defined.
	- The program cannot accept multiple input files, nor can it determine the type
		of input file it was given (ie. which program's results file was used as input).

Usage:
	./ortho_results_parser.py [-h] -i INPUT_FILE [-c] [-d] [-m] [-u] [-o OUT_NAME] [-v]
	OR
	python ortho_results_parser.py [-h] -i INPUT_FILE [-c] [-d] [-m] [-u] [-o OUT_NAME] [-v]
	
	Where the input files accepted are as follows: 
		- *.clustr file from CD-HIT
		- *.txt file from `diamond cluster`
		- *.tsv file from MMseqs2
		- *.uc file from USEARCH

This script was written for Python 3.9.18, in Spyder 5.4.3.

"""

#################################   ARGPARSE   #######################################
import argparse
# the argparse module allows for a single program script to be able to carry out a variety of specified functions
# this can be done with the specification of unique flags for each command


parser = argparse.ArgumentParser(description =
								 'This program takes an input results file from an orthologous clustering program,\
								 and performs pre-determined data restructuring and extraction processes on the file. \
								 Three results files will be produced: a JSON dictionary, an expanded pivot table, \
								 and a compressed comma-separated pivot table. \
								 The clustering software whose results files can be used as input are: \
								 CD-HIT, Diamond, MMseqs2 and USEARCH.')
# The most general description of what this program can do is defined here


# adding the arguments that the program can use
parser.add_argument(
	'-i', '--input',
	dest='input_file',
	metavar='INPUT_FILE',
	type=argparse.FileType('r'), 
	required=True,
	help='Provide this argument with your input file name.'
	)
	# the '-i' flag specifies the input file
parser.add_argument(
	'-c', '--cd_hit',
	action='store_true',
	help = 'This argument will parse the *.clstr results file from the CD-HIT program.'
	)
	# the '-c' flag will call for a CD-HIT results file to be parsed
parser.add_argument(
	'-d', '--diamond',
	action='store_true',
	help = 'This argument will parse the *.txt results file of the `diamond cluster` program.'
	)
	# the '-d' flag will call for a Diamond results file to be parsed
parser.add_argument(
	'-m', '--mmseqs2',
	action='store_true',
	help = 'This argument will parse the *.tsv results file of the MMseqs2 program.'
	)
	# the '-m' flag will call for a MMseqs2 results file to be parsed
parser.add_argument(
	'-u', '--usearch',
	action='store_true',
	help = 'This argument will parse the *.uc results file of the USEARCH program.'
	)
	# the '-u' flag will call for a CD-HIT results file to be parsed
parser.add_argument(
	'-o', '--outname',
	metavar='OUT_NAME',
	dest='out_name',
	help = 'This argument allows the user to define an output file basename. \n \
		The default basename is the basename of the input file.'
	)
	# the '-o' flag allows the user to define a the output file basename
parser.add_argument(
	'-v', '--version',
	action='version',
	version='%(prog)s 1.0'
	)
	# This portion of the code specifies the version of the program; currently 1.0
	# The user can call this flag ('-v') without specifying input and output files


args = parser.parse_args()
# this command allows the program to execute the arguments in the flags specified above


#################################   Main Program   ######################################


# Part 1: Import necessary modules

# import necessary modules
import os # allows access to the operating system
import pandas as pd # allows manipulation of dataframes in Python
import re # enables regex pattern matching
from string import punctuation # manipulate punctuation marks in strings
import json # allows import and export of data in JSON format


# Part 2: Determine input and output file names

# designate input file name as variable
input_ortho = args.input_file.name

# determine the output file basename
if args.out_name: 
	# if the user has specified an output basename to use
	# use that file name as the output file basename
	out_base = args.out_name
else: 
	# if no output file basename is provided
	base = os.path.basename(input_ortho)
	out_base = os.path.splitext(base)[0]

# establish the output file names
output_txt = out_base + "_parsed.txt"
output_pivot = out_base + "_parsed_pivot.txt"
output_json = out_base + "_parsed.json"


# Part 3: Parse input file & output results

# create empty dictionary to store orthologous cluster information
ortho_dict = {}


# parse arguments

if args.cd_hit:
	# if the user has given a CD-HIT input file
	with open(input_ortho, "r") as infile, open(output_txt, "w") as outfile_txt, open(output_pivot, "w") as outfile_pivot, open(output_json, "w") as outfile_json:
		# open the input and output files
		for line in infile: 
			# iterate over the input file line by line
			if line.startswith(">"): 
				# identify the sections that start a specific cluster ID
				cluster_id_tmp = line.strip()
				# strip the end line character from the cluster ID line
				cluster_id_tmp = re.sub(">", "CDH_", cluster_id_tmp)
				# remove the ">" character from the cluster ID name
				cluster_id = re.sub(" ", "_", cluster_id_tmp)
				# replace space in the cluster ID name with underscore
				# finally create an empty list to store cluster member IDs
				cluster_list = []
			else: 
				# if the line is a cluster member
				cluster_line = line.strip()
				# remove end-line character
				cluster_member_tmp = cluster_line.split(" ")[1]
				# extract the cluster member name
				cluster_member_tmp = re.sub(">", "", cluster_member_tmp)
				# remove the ">" character from the start of the name
				cluster_member = cluster_member_tmp.strip(punctuation)
				# remove the trailing periods from the end of the name
				# ref: https://stackoverflow.com/questions/37221307/how-do-i-strip-all-leading-and-trailing-punctuation-in-python
				cluster_list.append(cluster_member)
				# add the cluster member ID to the cluster membership list
			ortho_dict[cluster_id] = cluster_list
			# add the cluster information to the dictionary before moving to the next cluster
		# export the dictionary to a JSON file
		json.dump(ortho_dict, outfile_json)
		# convert dictionary to pandas dataframe in expanded form
		# ref: https://stackoverflow.com/questions/50751184/pandas-dataframe-from-dictionary-of-list-values
		ortho_pivot_df = pd.DataFrame([(key, var) for (key, L) in ortho_dict.items() for var in L], 
								columns=['CD-HIT_ID', 'CD-HIT_Members'])
		# write out the results to tab-separated text file
		ortho_pivot_df.to_csv(outfile_pivot, sep='\t', index=False, lineterminator='\n')
		# convert dictionary to pandas dataframe with lists in column
		# ref: https://stackoverflow.com/questions/33504424/pandas-dataframe-from-dictionary-with-lists
		ortho_df = pd.DataFrame([ortho_dict])
		# next need to flip the columns & rows
		# ref: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.transpose.html
		ortho_df = ortho_df.transpose()
		# pull the cluster ID column out of the index
		# ref: https://datatofish.com/index-to-column-pandas-dataframe/
		ortho_df.reset_index(inplace=True)
		# add/change the column names
		# ref: https://www.geeksforgeeks.org/add-column-names-to-dataframe-in-pandas/
		ortho_df.columns =['CD-HIT_ID', 'CD-HIT_Members']
		# turn the columns of lists into comma-separated strings
		# ref: https://stackoverflow.com/questions/45306988/column-of-lists-convert-list-to-string-as-a-new-column
		ortho_df['CD-HIT_Members'] = [','.join(map(str, l)) for l in ortho_df['CD-HIT_Members']]
		# export the pandas dataframe as a tab-separated text file
		ortho_df.to_csv(outfile_txt, sep='\t', index=False, lineterminator='\n')
		# last argument prevents random extra newlines between cluster info lines
		# ref: https://stackoverflow.com/questions/56398306/using-pandas-to-write-file-creates-blank-lines


if args.diamond or args.mmseqs2: 
	# same general parsing style can be used for Diamond or MMseqs2
	# so only the column names have to be specified
	if args.diamond: 
		# if the input file is from Diamond, name variables accordingly
		prog_clust_head = 'DMD_Cluster_'
		clust_id_col = 'Diamond_ID'
		clust_mem_col = 'Diamond_Members'
	if args.mmseqs2: 
		# if the input file is from MMseqs2, name variables accordingly
		prog_clust_head = 'MMS_Cluster_'
		clust_id_col = 'MMseqs2_ID'
		clust_mem_col = 'MMseqs2_Members'
	input_df = pd.read_csv(input_ortho, header = 0, sep = "\t")
	# read the input file into a pandas dataframe
	# and then set the column names
	# this is necessary to ensure the following section works for both Diamond & MMseqs2
	input_df.columns = ['centroid', 'member']
	# group dataframe to comma-separated strings per cluster
	ortho_df = input_df.groupby('centroid', as_index = False).agg(list)
	# pull the cluster ID column out of the index
	# ref: https://datatofish.com/index-to-column-pandas-dataframe/
	ortho_df.reset_index(inplace=True)
	# add cluster name identifier to the previous index column
	# ref: https://stackoverflow.com/questions/20025882/add-a-string-prefix-to-each-value-in-a-string-column-using-pandas
	ortho_df['index'] = prog_clust_head + ortho_df['index'].astype(str)
	# drop centroid id column
	ortho_df.drop('centroid', axis=1, inplace = True)
	# rename the columns
	ortho_df.columns = [clust_id_col, clust_mem_col]
	# convert the dataframe into a dictionary
	# ref: https://stackoverflow.com/questions/18695605/how-to-convert-a-dataframe-to-a-dictionary
	ortho_dict = dict(zip(ortho_df[clust_id_col], ortho_df[clust_mem_col]))
	with open(output_json, "w") as outfile_json:
		# open the JSON file for writing
		# and export the dictionary to a JSON file
		json.dump(ortho_dict, outfile_json)
	# convert dictionary to pandas dataframe in expanded form
	# ref: https://stackoverflow.com/questions/50751184/pandas-dataframe-from-dictionary-of-list-values
	ortho_pivot_df = pd.DataFrame([(key, var) for (key, L) in ortho_dict.items() for var in L], 
							columns=[clust_id_col, clust_mem_col])
	# write out the results to tab-separated text file
	ortho_pivot_df.to_csv(output_pivot, sep='\t', index=False, lineterminator='\n')
	# turn the columns of lists into comma-separated strings
	# ref: https://stackoverflow.com/questions/45306988/column-of-lists-convert-list-to-string-as-a-new-column
	ortho_df[clust_mem_col] = [','.join(map(str, l)) for l in ortho_df[clust_mem_col]]
	# export the pandas dataframe as a tab-separated text file
	ortho_df.to_csv(output_txt, sep='\t', index=False, lineterminator='\n')
	# last argument prevents random extra newlines between cluster info lines
	# ref: https://stackoverflow.com/questions/56398306/using-pandas-to-write-file-creates-blank-lines


if args.usearch: 
	# if the input file is from USEARCH
	with open(input_ortho, "r") as infile, open(output_txt, "w") as outfile_txt, open(output_pivot, "w") as outfile_pivot, open(output_json, "w") as outfile_json:
		# open the input and output files
		# create a counter to use to create cluster IDs
		counter = 0
		for line in infile: 
			# iterate over the input file line by line
			if line.startswith("S"): 
				# identify the sections that start a specific cluster ID
				centroid_id = line.strip().split("\t")[8]
				# strip the end line character from the cluster ID line
				# also split the elements of the line into a list
				# and select the sequence ID (pythonic index 8)
				cluster_id = "USR_Cluster_" + str(counter)
				# replace space in the cluster ID name with underscore
				# finally create an empty list to store cluster member IDs
				cluster_list = []
				# add the centroid sequence ID to the list
				cluster_list.append(centroid_id)
				# add +1 to the counter for the next iteration
				counter += 1
			elif line.startswith("H"): 
				# if the line is a cluster member
				cluster_member = line.strip().split("\t")[8]
				# strip the end line character from the line
				# also split the elements of the line into a list
				# and select the sequence ID (pythonic index 8)
				cluster_list.append(cluster_member)
				# add the cluster member ID to the cluster membership list
			ortho_dict[cluster_id] = cluster_list
			# add the cluster information to the dictionary before moving to the next cluster
		# export the dictionary to a JSON file
		json.dump(ortho_dict, outfile_json)
		# convert dictionary to pandas dataframe in expanded form
		# ref: https://stackoverflow.com/questions/50751184/pandas-dataframe-from-dictionary-of-list-values
		ortho_pivot_df = pd.DataFrame([(key, var) for (key, L) in ortho_dict.items() for var in L], 
								columns=['USEARCH_ID', 'USEARCH_Members'])
		# write out the results to tab-separated text file
		ortho_pivot_df.to_csv(outfile_pivot, sep='\t', index=False, lineterminator='\n')
		# convert dictionary to pandas dataframe with lists in column
		# ref: https://stackoverflow.com/questions/33504424/pandas-dataframe-from-dictionary-with-lists
		ortho_df = pd.DataFrame([ortho_dict])
		# next need to flip the columns & rows
		# ref: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.transpose.html
		ortho_df = ortho_df.transpose()
		# pull the cluster ID column out of the index
		# ref: https://datatofish.com/index-to-column-pandas-dataframe/
		ortho_df.reset_index(inplace=True)
		# add/change the column names
		# ref: https://www.geeksforgeeks.org/add-column-names-to-dataframe-in-pandas/
		ortho_df.columns =['USEARCH_ID', 'USEARCH_Members']
		# turn the columns of lists into comma-separated strings
		# ref: https://stackoverflow.com/questions/45306988/column-of-lists-convert-list-to-string-as-a-new-column
		ortho_df['USEARCH_Members'] = [','.join(map(str, l)) for l in ortho_df['USEARCH_Members']]
		# export the pandas dataframe as a tab-separated text file
		ortho_df.to_csv(outfile_txt, sep='\t', index=False, lineterminator='\n')
		# last argument prevents random extra newlines between cluster info lines
		# ref: https://stackoverflow.com/questions/56398306/using-pandas-to-write-file-creates-blank-lines
