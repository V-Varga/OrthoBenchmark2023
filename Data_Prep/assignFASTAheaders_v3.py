#!/bin/python
# -*- coding: utf-8 -*-
"""

Title: assignFASTAheaders_v3.py
Date: 2023.04.19
Author: Vi Varga

Description:
	This program replaces FASTA headers in a FASTA file with a 16-character random
		alphanumeric code. A reference file is also printed that links the
		random code to the original FASTA header. A larger reference file can also 
		be used as input and then appended to in order to ensure that no alphanumeric 
		header is repeated.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	re
	random
	string
	pandas

Procedure:
	1. Loading required modules & assigning command line argument.
    2. Contents of the large reference database are loaded into a Pandas dataframe,
		and existing alphanumeric headers are extracted to ensure no repitition.
	3. Parsing the input FASTA file in order to extract headers and generate
		random alphanumeric codes to replace them.
	4. Writing out the new FASTA file with the alphanumeric code headers,
		accompanied by the reference file.


Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- A reference file name must be given, even if the file does not exist yet. 

Source: 
    This script is based on the assignFASTAheaders_v2.py script written by the
        same author (Vi Varga) as part of their TrichoCompare MSc Thesis project
        work. The GitHub repository for this project is available here: 
        https://github.com/V-Varga/TrichoCompare

Version: 3.1
	The previous version of this script (assignFASTAheaders_v2.py) did not 
		include an option to create the reference file if it did not already 
		exist - it assumed the existence of the reference file. This script will
		create the reference file if it does not yet exist, or will append to it 
		if the file already exists. 
	Version 3.1 of this script also adds the source file name to the encoding 
		information in a third column. This functionality was added to account 
		for the fact that some FASTA headers are exactly repeated across files. 

Usage
	./assignFASTAheaders_v3.py input_fasta ref_file
	OR
	python assignFASTAheaders_v3.py input_fasta ref_file

This script was written for Python 3.9.16, in Spyder 5.4.3. 

"""


# Part 1: Import modules & assign command line arguments

#import necessary modules
import sys #allows execution of script from command line
import os #allow access to computer files
import re #enables regex pattern matching
import random #enables random number & variable generation
import string #imports a collection of string constants
import pandas as pd #allows manipulation of dataframes


#load input and output files
input_fasta = sys.argv[1]
#input_fasta = "Pseudomonas_aeruginosa_12-4-4_59_3618__EXTRACT.faa"
#assign the reference file to a variable
ref_db_file = sys.argv[2]
#ref_db_file = "PA_EncodingSummary.txt"
base = os.path.basename(input_fasta)
out_full = os.path.splitext(base)[0]
output_fasta = ".".join(input_fasta.split('.')[:-1]) + '_edit.fasta'


# Part 2: Assign the alphanumeric headers and write out results files

with open(input_fasta, "r") as infile, open(output_fasta, "w") as outfile:
	#open the input and output files
	#then determine if the reference file already exists
	if os.path.isfile(ref_db_file) == True:
		#if the reference file exists, open it to read and append
		ref_db = open(ref_db_file, "r+")
		#importing the large reference database into a Pandas dataframe
		ref_df = pd.read_csv(ref_db, sep="\t", header=None)
		encoding_list = ref_df[0].tolist()
	else: 
		#if the file doesn't already exist, create it
		ref_db = open(ref_db_file, "w")
		#create an empty list for the the new sequence IDs
		encoding_list = []
	#and now parse the files
	for line in infile:
		#iterate through the input file line by line
		if line.startswith(">"):
			#identify the header lines and remove the end-line character
			header = line.strip()
			#remove the ">" character at the start of the line
			#this enables easier manipulation of the FASTA header
			header = re.sub(">", "", header)
			while True:
				#generate a random 16-character alphanumeric string to replace the original header
				assigned_header = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
				if len(encoding_list) >= 0:
					#check if the reference database-derived encoding list exists
					#if it does, check that the same alphanumeric code hasn't already been used somewhere
					if assigned_header not in encoding_list:
						break
			#now print the new header to the outfile
			outfile.write(">" + assigned_header + "\n")
			#add the header to the large reference dataframe, along with the file basename
			ref_db.write(assigned_header + "\t" + header + "\t" + out_full + "\n")
		else:
			#sequence lines are copied to the outfile without changes
			outfile.write(line)

#close the opened reference file
ref_db.close()
