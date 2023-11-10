#!/bin/python
# -*- coding: utf-8 -*-
"""

Title: labelFASTA_dupes.py
Date: 2023.04.29
Author: Vi Varga

Description:
	This program parses a FASTA file containing duplicate FASTA header names 
		and makes them unique by adding " - Copy n" to the end of each 
		duplicate sequence starting from the first duplicate, where n is an
		integer >= 2.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	re

Procedure:
	1. Loading required modules & assigning command line argument.
    2. Parse the FASTA file and determine the copy number for duplicated sequence
		headers. Write out the sequence headers with information on the copy 
		number if the sequence header occurs more than once. 

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file names are not user-defined, but are instead based on the 
		input file name. 

Usage
	./labelFASTA_dupes.py input_fasta
	OR
	python labelFASTA_dupes.py input_fasta 

This script was written for Python 3.9.16, in Spyder 5.4.3. 

"""


# Part 1: Import modules & assign command line arguments

#import necessary modules
import sys #allows execution of script from command line
import re #enables regex pattern matching


#load input and output files
input_fasta = sys.argv[1]
#input_fasta = "Dupes_test_FASTA.fasta"
output_fasta = ".".join(input_fasta.split('.')[:-1]) + '_CopyN.fasta'


# Part 2: Assign the alphanumeric headers and write out results files

#create empty list for FASTA headers
header_list = []

#parse the FASTA files and change duplicate FASTA header names
with open(input_fasta, "r") as infile, open(output_fasta, "w") as outfile:
	#open the input file for reading and the output file for writing
	for line in infile:
		#iterate through the input file line by line
		if line.startswith(">"):
			#identify the header lines and remove the end-line character
			header = line.strip()
			#remove the ">" character at the start of the line
			#this enables easier manipulation of the FASTA header
			header = re.sub(">", "", header)
			#now check to see whether this FASTA header is a duplicate
			if header not in header_list:
				#if the header is not already in the list
				#add the header to the list of FASTA headers
				header_list.append(header)
				#and write the FASTA header out to the outfile as is
				outfile.write(">" + header + "\n")
			else: 
				#if the header is already in the list
				#count the number of times the header is already in the header list
				dupe_number = header_list.count(header)
				#add +1 to the value above
				copy_number = dupe_number + 1
				#and then still add the header to the list of FASTA headers
				header_list.append(header)
				#write out a new FASTA header to the file including the copy number
				outfile.write(">" + header + " - Copy " + str(copy_number) + "\n")
		else: 
			#for sequence lines
			#simply print the sequence line to the output file
			outfile.write(line)
