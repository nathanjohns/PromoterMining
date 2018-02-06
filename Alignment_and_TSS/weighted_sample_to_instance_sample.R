weighted_sample_to_instance_sample <- function(x, w_x){
#It returns a vector of sample instance from a weighted representation. This script was created to adapt .TSS input to ks.test();. 
#x is a vector of data values, and w_x indicates the frequency for the corresponding point in x.
#x <- c(1,4)
#w_x <- c(3,5)
#x_seq <- weighted_sample_to_instance_sample(x,w_x)
#x_seq will be : `1,1,1,4,4,4,4,4`
#
    n_x <- sum(w_x);
    x_seq <- vector(length=n_x);

    x_start <-1;
    for (i in 1:length(x)){
      if(w_x[i]==0){
        next;
      }
#        print(i);
        x_end <- x_start + w_x[i] - 1;
        x_seq[x_start:x_end] = x[i];
        x_start <- x_end + 1;
    }
    
    return( x_seq);
    
}
