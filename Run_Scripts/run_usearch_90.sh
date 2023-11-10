#!/bin/bash

###
# Title: run_usearch_90.sh
# Date: 2023.10.24
# Author: Vi Varga
#
# Description: 
# This script runs USEARCH to cluster the Pseudomonas aeruginosa
# genomes at 90%. 
# 
# Usage: 
# ./run_usearch_90.sh
# OR
# bash run_usearch_90.sh
#
# Note: 
# USEARCH is a licensed software installed globally on the Pheobe
# server. 
# 
###


### Set parameters
# Paths to key directories
MAINDIR=/storage/vivarga/OrthoBenchmark;
WORKDIR=$MAINDIR/Data;
OUTDIR=$MAINDIR/USEARCH_Results/Identity90;


### Run USEARCH
taskset --cpu-list 70-79 usearch \
-cluster_fast $WORKDIR/Concat_Pseudomonas_aeruginosa_CopyN_edit.fasta \
-id 0.90 -sort length -centroids $OUTDIR/Pa_CopyN_edit__centroids.fasta \
-consout $OUTDIR/Pa_CopyN_edit__consensus.fasta -uc $OUTDIR/Pa_CopyN_edit__clusters.uc \
-clusters $OUTDIR/Cluster_Dir/Cluster_ -threads 10;


# Program notes & references
# also setting specific threads to use with `taskset`
# ref: https://unix.stackexchange.com/questions/522765/parallel-running-with-only-limited-cpu-cores
# Notes on USEARCH commands
# Command manual: https://www.drive5.com/usearch/manual8.1/commands.html
# cluster_fast page: https://www.drive5.com/usearch/manual8.1/cmd_cluster_fast.html
# UCLUST algorithm ref: https://www.drive5.com/usearch/manual8.1/uclust_algo.html
# cluster_fast	 	Cluster sequences, optimized for speed.
# The -id option is an accept option that specifies the minimum sequence identity of a hit. It is expressed as a fraction between 0.0 and 1.0
# The -sort option will order to sort the input sequences for cluster_fast. Valid values are other (the default, meaning process sequences in the order they appear in the file), 
# length (sort by decreasing length) or size (sort by decreasing size annotation).
# centroids	 	Cluster centroids (FASTA).
# consout	 	Cluster consensus seqs. (FASTA).
# clusters	Directory to store FASTA files, one per cluster (cluster_fast only).
# uc	 	UCLUST-format tabbed text.
# threads	 	Number of threads (default: one per core).
