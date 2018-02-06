#This function uses a k-mean model to identify multiple TSS:
#
#This function starts with a `maximum` value for number of TSS.
#and re-iterates until it `converges` to number of TSS.
#It converges to n_TSS if it follows two criteria:
#
#1. distance between kmeans are greater than `dTSS_min`.
#2. Fraction in each kmean is greater than `frac_min`.
#
source("weighted_sample_to_instance_sample.R");

multiple_tss_prediction_optimized <- function( TSS_raw_file, n_cluster_max=6, dTSS_min=5, frac_min=0.1, save_path=F, save_str="" ){
  
  rt <- read.table(TSS_raw_file);
  names(rt) <- c("promoter_id", "TSS_position", "TSS_distribution");
  promoter_id_set = sort(unique(rt$promoter_id));
  l = length(promoter_id_set);
  
  data <- matrix(nrow=l,ncol=5); #promoter_id, n_TSS, k_means, frac_in_k_mean, total_reads; 
  colnames(data) = 1:5;
  colnames(data)<- c("promoter_id", "n_TSS", "k_means", "frac_in_k_mean", "total_reads");
  
  for (i in 1:l){
    if(i%%round(l/10)==0){
      print(sprintf("%2.2f%%",i/l*100));
    }
    
    cur_n_TSS=n_cluster_max;
    cur_promoter_id <- promoter_id_set[i];
    
    cur_TSS_position <- rt$TSS_position[ rt$promoter_id == cur_promoter_id];
    cur_TSS_distribution <- rt$TSS_distribution[ rt$promoter_id == cur_promoter_id];
    
    while( length(cur_TSS_position) < cur_n_TSS){
    	cur_n_TSS=cur_n_TSS-1;
    }
    if(sum(cur_TSS_distribution)==cur_n_TSS){
      cur_n_TSS=cur_n_TSS-1;
    }
    
    TSS_position_as_vector <- weighted_sample_to_instance_sample(cur_TSS_position, cur_TSS_distribution);
    

    is_done=0;
    cur_reads_total=length(TSS_position_as_vector);
    while(!is_done & cur_n_TSS>0){
    	
    	cur_k_mean_set <- kmeans(TSS_position_as_vector, cur_n_TSS);
    	
    	dTSS <- diff(sort(cur_k_mean_set$centers));
    	#cur_reads_total=sum(cur_k_mean_set$size);
    	frac_in_k_mean <- cur_k_mean_set$size/cur_reads_total;
    	if( any(dTSS<dTSS_min) | any(frac_in_k_mean<frac_min) ){
    		cur_n_TSS=cur_n_TSS-1;
    	}
    	else{
    		is_done=1;
		}
	} 
   
    if(cur_n_TSS>0){
    	centers_str <- paste(sprintf("%2.2f",cur_k_mean_set$centers),collapse=";");
    	frac_str <- paste(sprintf("%2.2f",frac_in_k_mean),collapse=";");
    }
    else{
	centers_str=cur_TSS_position;
	frac_str=1;
    } 
    
    data[i,1] <- cur_promoter_id
    data[i,2] <- cur_n_TSS;
    data[i,3] <- centers_str;
    data[i,4] <- frac_str;
    data[i,5] <- cur_reads_total;
 
  }
  
   
  if(save_path!=F){
    save_file = sprintf("%s%s_nTSSmax=%d_dTSS_min%d_fracmin%2.2f.txt",
    save_path, save_str,
    n_cluster_max, dTSS_min,frac_min);
    write.table(data, save_file,row.names = F,quote = F );    
  }
 
 return(data);
 
}

#TSS_raw_file <- "/home/alg2199/projects/hpt/analysis/TSS/R2_all/2014-03-20_E.c._LB.TSS";
#n_cluster <- 2;
#k_mean_set <- multiple_tss_prediction(TSS_raw_file, n_cluster,save_path="/home/alg2199/","temp");

