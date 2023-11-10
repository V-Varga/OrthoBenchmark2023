#!/usr/bin/env Rscript

###

# Title: visualize_desc_stats.R
# Date: 2023.10.29
# Author: Vi Varga
# 
# Description:
#   This program plots scatterplots, boxplots & violin plots relating to 
#     descriptive statistics on the OrthoBenchmark pipeline. 
# 
# List of functions:
#   No functions are defined in this script.
# 
# List of standard and non-standard libraries used:
#   tidyverse
#   ggplot2
#   scales
#   svglite
#   reshape2
#   viridis
# 
# Procedure:
#   1. Load necessary libraries
#   2. Load data files into R
#   3. Perform data wrangling & plot descriptive statistics in scatterplots
#   4. Perform data wrangling & create boxplots & violin plots
#   5. Cluster overlap heatmap - TBD, may be in future update
# 
# Known bugs and limitations:
#   - There is no quality-checking integrated into the code.
#   - The output file name is not entirely user-defined, but is instead based on the input
#     file name.
# 
# Usage: 
#   Run selected portions of this script from within RStudio to render output graphics files. 
# 
# This script was written for R version 4.3.1 (2023-06-16 ucrt), in RStudio 2023.09.1+494 
#   "Desert Sunflower". 

###


# Part 1: Load necessary libraries & assign command-line arguments

# setting up the workspace
# clear the environment
rm(list = ls())

# load libraries
library(tidyverse)
library(ggplot2)
library(scales)
library(reshape2)
library(svglite)
library(viridis)


# Parse command line arguments
# enable command line input
#args <- commandArgs(trailingOnly = TRUE)

# get the input file name
#infile_stats <- args[1]
infile_stats <- "C:/Users/viragv/Documents/ChalmersG/Clustering/OrthoBenchmark/ProgramResults/Orthology_Comparison_Stats__07-11-2023--195750.txt"
#infile_counts <- args[2]
infile_counts <- "C:/Users/viragv/Documents/ChalmersG/Clustering/OrthoBenchmark/ProgramResults/Ortho_Comparison_CountsClean__07-11-2023--123116.txt"
#infile_data <- args[3]
#infile_data <- "C:/Users/viragv/Documents/ChalmersG/Clustering/OrthoBenchmark/ProgramResults/Orthology_Comparison_DB__26-10-2023--174514.txt"

# extract the actual file name from the full name that includes the path
infile_name <- basename(infile_stats)
infile_name_counts <- basename(infile_counts)
#infile_name_data <- basename(infile_data)
# set the working directory to where the input file is located
setwd(dirname(infile_stats))

# determine the output file name based on the input file name
outfile_basename <- paste((str_split(infile_name, "__")[[1]][1]), "Visualized", sep = "__")


# Part 2: Import data table

# load the data into dataframes in R
stats_table <- read.delim(infile_name, header = TRUE, sep = '\t')
counts_table <- read.delim(infile_name_counts, header = TRUE, sep = '\t')
#data_big_table <- read.delim(infile_name_data, header = TRUE, sep = '\t')

# add grouping categories to stats_table
# first duplicate the clustering program types
# ref: https://stackoverflow.com/questions/22030252/duplicate-a-column-in-data-frame-and-rename-it-to-another-column-name
stats_table$Clust_Percent = stats_table$OG_Source
# edit strings in new column to only contain percent identity values
# ref: https://stackoverflow.com/questions/25277117/remove-part-of-a-string-in-dataframe-column-r
# ref: https://stackoverflow.com/questions/12297859/remove-all-text-before-colon
stats_table$Clust_Percent <- gsub(".*Pa_", "", stats_table$Clust_Percent)
# create a new column for the program names
# ref: https://datascience.stackexchange.com/questions/8922/removing-strings-after-a-certain-character-in-a-given-text
stats_table$Program_Name <- gsub("_.*", "", stats_table$OG_Source)
# remove '_Pa_' substring from first column
# ref: https://www.r-bloggers.com/2022/07/how-to-replace-string-in-column-in-r/
stats_table$OG_Source_Clean <- str_replace(stats_table$OG_Source, '_Pa_', ' ')


# Part 3: Plot descriptive statistics

# create list of color IDs from Viridis
# ref: https://www.thinkingondata.com/something-about-viridis-library/
color_list <- viridis_pal()(5)
# use first 3 colors from this list
# ref: https://stackoverflow.com/questions/12114439/remove-the-last-element-of-a-vector
color_list <- head(color_list, -2)


# Cluster number
# ref: https://stackoverflow.com/questions/8592585/combine-points-with-lines-with-ggplot2
# ref: https://r-charts.com/ggplot2/titles/
# ref: https://www.r-bloggers.com/2021/09/how-to-rotate-axis-labels-in-ggplot2/
# ref: https://stackoverflow.com/questions/14563989/force-r-to-stop-plotting-abbreviated-axis-labels-scientific-notation-e-g-1e
# ref: https://stackoverflow.com/questions/14622421/how-to-change-legend-title-in-ggplot
# ref: http://www.sthda.com/english/wiki/ggplot2-point-shapes
# ref: https://www.datanovia.com/en/blog/ggplot-point-shapes-best-tips/
# ref: https://ggplot2.tidyverse.org/reference/scale_viridis.html
# ref: https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html
# ref: http://www.sthda.com/english/wiki/ggplot2-colors-how-to-change-colors-automatically-and-manually

plot_clustnum <- ggplot(stats_table, aes(x = OG_Source_Clean, y = Cluster_Num, color = Clust_Percent, group = Clust_Percent)) + 
  geom_point(aes(shape = Program_Name), size = 4.5) + geom_line() + 
  labs(title = "Number of Clusters", subtitle = "Per clustering program & percent identity", 
       y = "Number of clusters", x = "Clustering program & threshold", color = "Clustering \nPercent Identity", 
       shape = "Clustering \nProgram") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 14), 
        text = element_text(size = 18)) +
  scale_y_continuous(labels = comma) +
  scale_shape_manual(values = c(15, 18, 17, 16)) +
  #scale_colour_viridis_d(option = "viridis") +
  scale_color_manual(values=color_list)

# Maximum cluster size
plot_maxsize <- ggplot(stats_table, aes(x = OG_Source_Clean, y = Max_Size, color = Clust_Percent, group = Clust_Percent)) + 
  geom_point(aes(shape = Program_Name), size = 4.5) + geom_line() + 
  labs(title = "Maximum Cluster Size", subtitle = "Per clustering program & percent identity", 
       y = "Maximum cluster size", x = "Clustering program & threshold", color = "Clustering \nPercent Identity", 
       shape = "Clustering \nProgram") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 14), 
        text = element_text(size = 18)) +
  scale_y_continuous(labels = comma) +
  scale_shape_manual(values = c(15, 18, 17, 16)) +
  #scale_colour_viridis_d(option = "viridis") +
  scale_color_manual(values=color_list)

# Mean cluster size
plot_mean <- ggplot(stats_table, aes(x = OG_Source_Clean, y = Avg_Mean_Size, color = Clust_Percent, group = Clust_Percent)) + 
  geom_point(aes(shape = Program_Name), size = 4.5) + geom_line() + 
  labs(title = "Mean Cluster Size", subtitle = "Per clustering program & percent identity", 
       y = "Mean cluster size", x = "Clustering program & threshold", color = "Clustering \nPercent Identity", 
       shape = "Clustering \nProgram") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 14), 
        text = element_text(size = 18)) +
  scale_y_continuous(labels = comma) +
  scale_shape_manual(values = c(15, 18, 17, 16)) +
  #scale_colour_viridis_d(option = "viridis") +
  scale_color_manual(values=color_list)

# Median cluster size
plot_median <- ggplot(stats_table, aes(x = OG_Source_Clean, y = Median_Size, color = Clust_Percent, group = Clust_Percent)) + 
  geom_point(aes(shape = Program_Name), size = 4.5) + geom_line() + 
  labs(title = "Median Cluster Size", subtitle = "Per clustering program & percent identity", 
       y = "Median cluster size", x = "Clustering program & threshold", color = "Clustering \nPercent Identity", 
       shape = "Clustering \nProgram") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 14), 
        text = element_text(size = 18)) +
  scale_y_continuous(labels = comma) +
  scale_shape_manual(values = c(15, 18, 17, 16)) +
  #scale_colour_viridis_d(option = "viridis") +
  scale_color_manual(values=color_list)

# Mode cluster size
plot_mode <- ggplot(stats_table, aes(x = OG_Source_Clean, y = Mode_Size, color = Clust_Percent, group = Clust_Percent)) + 
  geom_point(aes(shape = Program_Name), size = 4.5) + geom_line() + 
  labs(title = "Mode Cluster Size", subtitle = "Per clustering program & percent identity", 
       y = "Mode cluster size", x = "Clustering program & threshold", color = "Clustering \nPercent Identity", 
       shape = "Clustering \nProgram") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 14), 
        text = element_text(size = 18)) +
  scale_y_continuous(labels = comma) +
  scale_shape_manual(values = c(15, 18, 17, 16)) +
  #scale_colour_viridis_d(option = "viridis") +
  scale_color_manual(values=color_list)

# Standard deviation in cluster size
plot_stddev <- ggplot(stats_table, aes(x = OG_Source_Clean, y = Std_Dev, color = Clust_Percent, group = Clust_Percent)) + 
  geom_point(aes(shape = Program_Name), size = 4.5) + geom_line() + 
  labs(title = "Standard Deviation in Cluster Size", subtitle = "Per clustering program & percent identity", 
       y = "Standard deviation in cluster size", x = "Clustering program & threshold", 
       color = "Clustering \nPercent Identity", shape = "Clustering \nProgram") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 14), 
        text = element_text(size = 18)) +
  scale_y_continuous(labels = comma) +
  scale_shape_manual(values = c(15, 18, 17, 16)) +
  #scale_colour_viridis_d(option = "viridis") +
  scale_color_manual(values=color_list)

# Variance in cluster size
plot_variance <- ggplot(stats_table, aes(x = OG_Source_Clean, y = Variance, color = Clust_Percent, group = Clust_Percent)) + 
  geom_point(aes(shape = Program_Name), size = 4.5) + geom_line() + 
  labs(title = "Variance in Cluster Size", subtitle = "Per clustering program & percent identity", 
       y = "Variance in cluster size", x = "Clustering program & threshold", color = "Clustering \nPercent Identity", 
       shape = "Clustering \nProgram") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 14), 
        text = element_text(size = 18)) +
  scale_y_continuous(labels = comma) +
  scale_shape_manual(values = c(15, 18, 17, 16)) +
  #scale_colour_viridis_d(option = "viridis") +
  scale_color_manual(values=color_list)

# Number of singletons
plot_singletons <- ggplot(stats_table, aes(x = OG_Source_Clean, y = Singleton_Num, color = Clust_Percent, group = Clust_Percent)) + 
  geom_point(aes(shape = Program_Name), size = 4.5) + geom_line() + 
  labs(title = "Number of Single-Protein Clusters", subtitle = "Per clustering program & percent identity", 
       y = "Number of singletons", x = "Clustering program & threshold", color = "Clustering \nPercent Identity", 
       shape = "Clustering \nProgram") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 14), 
        text = element_text(size = 18)) +
  scale_y_continuous(labels = comma) +
  scale_shape_manual(values = c(15, 18, 17, 16)) +
  #scale_colour_viridis_d(option = "viridis") +
  scale_color_manual(values=color_list)


# printing the results to files
# open PDF file for printing of all plots to one file
# ref: https://stackoverflow.com/questions/1395410/how-to-print-r-graphics-to-multiple-pages-of-a-pdf-and-multiple-pdfs
# ref: https://www.rdocumentation.org/packages/grDevices/versions/3.6.2/topics/pdf
pdf(paste(outfile_basename, "pdf", sep = "."))
plot_clustnum
plot_maxsize
plot_mean
plot_median
plot_mode
plot_stddev
plot_variance
plot_singletons
dev.off()

# print individually to SVG files
# ref: https://www.rdocumentation.org/packages/svglite/versions/2.1.0/topics/svglite
svglite(paste(paste(outfile_basename, "ClustNum", sep = "__"), "svg", sep = "."), width = 10, height = 8)
plot_clustnum
dev.off()

svglite(paste(paste(outfile_basename, "MaxClustSize", sep = "__"), "svg", sep = "."), width = 10, height = 8)
plot_maxsize
dev.off()

svglite(paste(paste(outfile_basename, "MeanClustSize", sep = "__"), "svg", sep = "."), width = 10, height = 8)
plot_mean
dev.off()

svglite(paste(paste(outfile_basename, "MedianClustSize", sep = "__"), "svg", sep = "."), width = 10, height = 8)
plot_median
dev.off()

svglite(paste(paste(outfile_basename, "ModeClustSize", sep = "__"), "svg", sep = "."), width = 10, height = 8)
plot_mode
dev.off()

svglite(paste(paste(outfile_basename, "StdDevClustSize", sep = "__"), "svg", sep = "."), width = 10, height = 8)
plot_stddev
dev.off()

svglite(paste(paste(outfile_basename, "VarianceClustSize", sep = "__"), "svg", sep = "."), width = 10, height = 8)
plot_variance
dev.off()

svglite(paste(paste(outfile_basename, "SingletonNum", sep = "__"), "svg", sep = "."), width = 10, height = 8)
plot_singletons
dev.off()


# Part 4: Box-and-whisker distribution plots of cluster size

# fix header structures
# ref: https://stackoverflow.com/questions/16041935/remove-dots-from-column-names
names(counts_table) <- gsub(".", "-", names(counts_table), fixed=TRUE)
names(counts_table) <- gsub("_", " ", names(counts_table), fixed=TRUE)
names(counts_table) <- gsub("Pa ", "", names(counts_table), fixed=TRUE)
names(counts_table) <- gsub(" counts", "", names(counts_table), fixed=TRUE)


# create boxplots of each column
# ref: https://stackoverflow.com/questions/15071334/boxplot-of-table-using-ggplot2
# regular scale
plot_boxreg <- ggplot(data = melt(counts_table), aes(x=variable, y=value)) + 
  geom_boxplot(aes(fill=variable)) + 
  labs(title = "Distribution of cluster sizes", y = "Cluster sizes", x = "Clustering program & threshold", 
       fill = "Clustering Program & \nPercent Identity") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 14), 
        text = element_text(size = 18))

# log scale
plot_boxlog <- ggplot(data = melt(counts_table), aes(x=variable, y=value)) + 
  geom_boxplot(aes(fill=variable)) + 
  labs(title = "Distribution of cluster sizes", y = "Cluster sizes (log10)", x = "Clustering program & threshold", 
       fill = "Clustering Program & \nPercent Identity") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 14), 
        text = element_text(size = 18)) +
  scale_y_continuous(trans='log10')

# violin plot
# regular scale
plot_violinreg <- ggplot(data = melt(counts_table), aes(x=variable, y=value)) + 
  geom_violin(aes(fill=variable)) + 
  labs(title = "Distribution of cluster sizes", y = "Cluster sizes", x = "Clustering program & threshold", 
       fill = "Clustering Program & \nPercent Identity") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 14), 
        text = element_text(size = 18))

# log scale
plot_violinlog <- ggplot(data = melt(counts_table), aes(x=variable, y=value)) + 
  geom_violin(aes(fill=variable)) + 
  labs(title = "Distribution of cluster sizes", y = "Cluster sizes (log10)", x = "Clustering program & threshold", 
       fill = "Clustering Program & \nPercent Identity") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1, size = 14), 
        text = element_text(size = 18)) +
  scale_y_continuous(trans='log10')


# Print results to files
# open PDF for printing
pdf(paste(paste(outfile_basename, "Boxplots", sep = "__"), "pdf", sep = "."))
plot_boxreg
plot_boxlog
plot_violinreg
plot_violinlog
dev.off()


# print individual plots to SVG files
svglite(paste(paste(outfile_basename, "BoxplotReg", sep = "__"), "svg", sep = "."), width = 10, height = 8)
plot_boxreg
dev.off()

svglite(paste(paste(outfile_basename, "BoxplotLog", sep = "__"), "svg", sep = "."), width = 10, height = 8)
plot_boxlog
dev.off()

svglite(paste(paste(outfile_basename, "ViolinReg", sep = "__"), "svg", sep = "."), width = 10, height = 8)
plot_violinreg
dev.off()

svglite(paste(paste(outfile_basename, "ViolinLog", sep = "__"), "svg", sep = "."), width = 10, height = 8)
plot_violinlog
dev.off()


# Part 5: Heatmap of cluster overlap data

# TBD
