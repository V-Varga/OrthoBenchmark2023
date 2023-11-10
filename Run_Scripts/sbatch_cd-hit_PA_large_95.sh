#!/usr/bin/env bash

#SBATCH -A C3SE2023-1-21 -p vera
#SBATCH -N 1
#SBATCH -C MEM512
#SBATCH -t 03:00:00
#SBATCH -J cd-hit_clust
#SBATCH --mail-user=virag.varga@chalmers.se
#SBATCH --mail-type=ALL
# Set the names for the error and output files
#SBATCH --error=job.%J.err
#SBATCH --output=job.%J.out


###
# Title: sbatch_cd-hit_PA_large_95.sh
# Date: 2023.10.24
# Author: Vi Varga
#
# Description: 
# This script will run the CD-HIT on C3SE Vera from the env-cd-hit.sif
# Apptainer container file, on the _Pseudomonas aeruginosa_ strains collected
# from the pseudomonas.com database.
# 
# Usage: 
# sbatch sbatch_cd-hit_PA_large_95.sh
###


### Set parameters
# key directories
MAINDIR=/cephyr/NOBACKUP/groups/jbp/vivarga/ARGs_Invasion;
WORKDIR=$MAINDIR/Data;
OUTDIR=$MAINDIR/Orthology/CD-HIT_Results/Identity95;

# files used
CONTAINER_LOC=$MAINDIR/bin/env-cd-hit.sif;
WORKING_TMP=$TMPDIR/CD-HIT_TMP;
RESULTS_TMP=$WORKING_TMP/Results;


### Load modules
module purge
#module load MODULE_NAME/module.version ...;


# Copy relevant files to $TMPDIR
mkdir $WORKING_TMP;
mkdir $RESULTS_TMP;
cp $CONTAINER_LOC $WORKING_TMP;
cp $WORKDIR/Concat_Pseudomonas_aeruginosa_CopyN_edit.fasta $WORKING_TMP;
cd $RESULTS_TMP;


### Runing CD-HIT
apptainer exec $WORKING_TMP/env-cd-hit.sif cd-hit -i $WORKING_TMP/Concat_Pseudomonas_aeruginosa_CopyN_edit.fasta \
-o $RESULTS_TMP/Concat_Pseudomonas_aeruginosa_CopyN_edit_95 -c 0.95 -n 5 -M 1000000 -T 64 -p 1 -g 1;


### Copy relevant files back, SLURM_SUBMIT_DIR is set by SLURM
cp -r $RESULTS_TMP/* $OUTDIR;


# Refs: 
# C3SE container use: https://www.c3se.chalmers.se/documentation/applications/containers/
# CD-HIT usage instructions: https://github.com/weizhongli/cdhit/wiki
# -i	input filename in fasta format, required
# -o	output filename, required
# -c	sequence identity threshold, default 0.9
# -n	word_length, default 5; -n 5 for thresholds 0.7 ~ 1.0
# -M	memory limit (in MB) for the program, default 800; 0 for unlimitted
# -d	length of description in .clstr file, default 20 if set to 0, it takes the fasta defline and stops at first space
# -T	number of threads, default 1; with 0, all CPUs will be used
# -p	1 or 0, default 0 if set to 1, print alignment overlap in .clstr file
# -g	1 or 0, default 0 by cd-hit's default algorithm, a sequence is clustered to the first cluster that meet the threshold 
# (fast cluster). If set to 1, the program will cluster it into the most similar cluster that meet the threshold (accurate but slow mode)
