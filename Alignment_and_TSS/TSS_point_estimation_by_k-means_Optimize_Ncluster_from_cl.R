#This script computes `TSS`s from file. It permits estimating multiple TSS from same file.
#
#TSS_raw_file <- "/home/alg2199/projects/hpt/analysis/TSS/R2_all/2014-03-20_E.c._LB.TSS";
#n_cluster <- 2;
#k_mean_set <- multiple_tss_prediction(TSS_raw_file, n_cluster,save_path="/home/alg2199/","temp");

source("TSS_point_estimation_by_k-means_Optimize_Ncluster.R");

args <- commandArgs(trailingOnly=TRUE);

TSS_raw_file <- args[1];
n_cluster_max = 6;# <- as.numeric(args[2]); #2;
save_path="";
#save_path="/usr/local/home/alg2199/projects/hpt/analysis/TSS/R2_all/fixed/kmean/";
#pre_tag_str = strsplit(TSS_raw_file,"/");
#tag_str = strsplit(pre_tag_str[[1]][length(pre_tag_str[[1]])],".TSS");
save_str=sprintf("%s",TSS_raw_file);
#print(save_str);

print("1");
k_mean_set <- multiple_tss_prediction_optimized(TSS_raw_file, 
                                                n_cluster_max=n_cluster_max, 
                                                dTSS_min=5,
                                                frac_min=0.1,
                                                save_path,
                                                save_str);