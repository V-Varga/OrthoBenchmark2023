#!/usr/bin/env bash

#SBATCH -A C3SE2023-1-21 -p vera
#SBATCH -N 1
#SBATCH -C MEM512
#SBATCH -t 03:00:00
#SBATCH -J mmseqs2_clust
#SBATCH --mail-user=virag.varga@chalmers.se
#SBATCH --mail-type=ALL
# Set the names for the error and output files
#SBATCH --error=job.%J.err
#SBATCH --output=job.%J.out


###
# Title: sbatch_mmseqs2_PA_large_95.sh
# Date: 2023.10.20
# Author: Vi Varga
#
# Description: 
# This script will run the MMseqs2 on C3SE Vera from the env-mmseqs2.sif
# Apptainer container file, on the _Pseudomonas aeruginosa_ strains collected
# from the pseudomonas.com database.
# 
# Usage: 
# sbatch sbatch_mmseqs2_PA_large_95.sh
###


### Set parameters
# key directories
MAINDIR=/cephyr/NOBACKUP/groups/jbp/vivarga/ARGs_Invasion;
WORKDIR=$MAINDIR/Data;
OUTDIR=$MAINDIR/Orthology/MMseqs2_Results/Identity95;

# files used
CONTAINER_LOC=$MAINDIR/bin/env-mmseqs2.sif;
WORKING_TMP=$TMPDIR/MMseqs2_TMP;


### Load modules
module purge
#module load MODULE_NAME/module.version ...;


# Copy relevant files to $TMPDIR
mkdir $WORKING_TMP;
cp $CONTAINER_LOC $WORKING_TMP;
cp $WORKDIR/Concat_Pseudomonas_aeruginosa_CopyN_edit.fasta $WORKING_TMP;
cd $WORKING_TMP;
mkdir $WORKING_TMP/Results;
cd $WORKING_TMP/Results;


### Runing MMseqs2
# create MMseqs2 database
apptainer exec $WORKING_TMP/env-mmseqs2.sif mmseqs createdb $WORKING_TMP/Concat_Pseudomonas_aeruginosa_CopyN_edit.fasta Pa_DB_95;

# cluster the database
mkdir $WORKING_TMP/Results/tmp;
apptainer exec $WORKING_TMP/env-mmseqs2.sif mmseqs cluster Pa_DB_95 Pa_DB_95_clu tmp --min-seq-id 0.95 --threads 64;

# generate a TSV file of the results
apptainer exec $WORKING_TMP/env-mmseqs2.sif mmseqs createtsv Pa_DB_95 Pa_DB_95 Pa_DB_95_clu Pa_DB_95_clu.tsv --threads 64;


### Copy relevant files back, SLURM_SUBMIT_DIR is set by SLURM
cp -r $WORKING_TMP/Results/* $OUTDIR;


# Refs: 
# C3SE container use: https://www.c3se.chalmers.se/documentation/applications/containers/
# MMseqs2 GitHub page: https://github.com/soedinglab/MMseqs2
# MMseqs2 usage guide: https://github.com/soedinglab/mmseqs2/wiki
# MMseqs clustering: https://github.com/soedinglab/mmseqs2/wiki#clustering
# createdb              Convert FASTA/Q file(s) to a sequence DB
# cluster               Slower, sensitive clustering
# --min-seq-id FLOAT              List matches above this sequence identity (for clustering) (range 0.0-1.0) [0.000]
# createtsv             Convert result DB to tab-separated flat file
# --threads INT                   Number of CPU-cores used (all by default) [32]
