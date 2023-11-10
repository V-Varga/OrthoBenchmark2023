#!/usr/bin/env bash

#SBATCH -A C3SE2023-1-21 -p vera
#SBATCH -N 1
#SBATCH -C MEM512
#SBATCH -t 03:00:00
#SBATCH -J diamond_clust
#SBATCH --mail-user=virag.varga@chalmers.se
#SBATCH --mail-type=ALL
# Set the names for the error and output files
#SBATCH --error=job.%J.err
#SBATCH --output=job.%J.out


###
# Title: sbatch_diamond_PA_large_90.sh
# Date: 2023.08.23
# Author: Vi Varga
#
# Description: 
# This script will run the Diamond on C3SE Vera from the env-diamond.sif
# Apptainer container file, on the _Pseudomonas aeruginosa_ strains collected
# from the pseudomonas.com database.
# 
# Usage: 
# sbatch sbatch_diamond_PA_large_90.sh
###


### Set parameters
# key directories
MAINDIR=/cephyr/NOBACKUP/groups/jbp/vivarga/ARGs_Invasion;
WORKDIR=$MAINDIR/Data;
OUTDIR=$MAINDIR/Orthology/Diamond_Results/Identity90;

# files used
DMD_LOC=$MAINDIR/bin/env-diamond.sif;
DIAMOND_TMP=$TMPDIR/DIAMOND_Pa;


### Load modules
module purge
#module load MODULE_NAME/module.version ...;


# Copy relevant files to $TMPDIR
mkdir $DIAMOND_TMP;
cp $DMD_LOC $DIAMOND_TMP;
cp $WORKDIR/Concat_Pseudomonas_aeruginosa_CopyN_edit.fasta $DIAMOND_TMP;
cd $DIAMOND_TMP;


### Runing Diamond
apptainer exec $DIAMOND_TMP/env-diamond.sif diamond cluster -d $DIAMOND_TMP/Concat_Pseudomonas_aeruginosa_CopyN_edit.fasta \
-o $DIAMOND_TMP/PA_diamond_clust.txt --header --approx-id 90 -M 975G -p 60 --log;


# Copy relevant files back, SLURM_SUBMIT_DIR is set by SLURM
cp $DIAMOND_TMP/PA_diamond_clust.txt $OUTDIR;
cp $DIAMOND_TMP/diamond.log $OUTDIR;


# Refs: 
# C3SE container use: https://www.c3se.chalmers.se/documentation/applications/containers/
# Diamond GitHub: https://github.com/bbuchfink/diamond
# Diamond usage Wiki: https://github.com/bbuchfink/diamond/wiki
# Diamond clustering: https://github.com/bbuchfink/diamond/wiki/Clustering
# --database/-d : The input sequence database. Supported formats are FASTA and DIAMOND (.dmnd) format.
# --out/-o : Output file. This is a 2-column tabular file with the representative accession as the first column 
# and the member sequence accession as the second column. More elaborate output can be retrieved using the realign workflow.
# --header : Enable a header line in the output file.
# --memory-limit/-M # : Set a memory limit for the diamond process (for example: -M 64G). This is not a hard upper limit 
# and may still be exceeded in certain cases. Decrease this number in case the tool fails due to running out of memory. 
# Note that higher numbers increase the performance by a lot, so it is strongly recommended to always set this option. 
# Note that this option affects the algorithm and therefore the results. Clustering is a heuristic procedure with no unique solution.
# --approx-id # : The identity cutoff for the clustering (in %). Note that for performance reasons, the setting refers to the 
# approximate sequence identity derived as a linear regression from the bitscore, not the actual number of identities in the alignment. 
# The default value is 50% when running diamond cluster and 0% when running diamond deepclust.
# --member-cover # : The minimum coverage of the cluster member sequence by the representative (in %). 
# This is a unidirectional coverage i.e. a minimum coverage of the representative is not required. The default is 80%.
# --threads/-p # : Number of CPU threads. By default, the program will auto-detect and use all available virtual cores on the machine.
# --log : Enable even more verbose terminal output, which is also written to a file named diamond.log is the current working directory.
