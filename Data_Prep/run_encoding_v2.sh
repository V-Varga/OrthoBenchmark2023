#!/bin/bash

###
# Title: run_encoding_v2.sh
# Date: 2023.04.29
# Author: Vi Varga
#
# Description: 
# This script runs the assignFASTAheaders_v3.py script in a loop on the *.faa 
# files in the ARGs_Invasion project. 
# 
# Usage: 
# ./run_encoding_v2.sh
# OR
# bash run_encoding_v2.sh
###


ls /storage/vivarga/ARGs_Invasion/Data/PA_faa/*_CopyN.fasta | while read file; do
  full_file="${file##*/}"; #this line removes the path before the file name
  file_base="${full_file%.*}"; #this line removes the file extension
  python /storage/vivarga/ARGs_Invasion/Scripts/assignFASTAheaders_v3.py $file /storage/vivarga/ARGs_Invasion/Data/PA_EncodingSummary.txt;
  mv /storage/vivarga/ARGs_Invasion/Data/PA_faa/${file_base}_edit.fasta /storage/vivarga/ARGs_Invasion/Data/Edited_faa/ ;
  echo $file >> /storage/vivarga/ARGs_Invasion/Data/CompletedEncoding.txt;
done
