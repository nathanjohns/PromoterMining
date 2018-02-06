#Test if test_R1_data can align to promoter sequence

library("Biostrings");
library("R.utils"); #function countLines.
source("parse_alignment.R")

get_alignment_score_and_TSS <- function(bc_data_file, promoter_sequence_file = "promoter_plus_ATG_plus_barcode.txt", direction, output_file, read_start_position=1)
{
#bc_data_file is file input from Anthony's script.
#direction "R1" uses reverse complement of promoters; "R2" uses standard.
#The default promoter_sequence file is: promoter_plus_ATG_plus_barcode.txt.
#read_start_position: start position from read output. It gets on position 0  

rt <- read.table(promoter_sequence_file);
promoter_sequence <- as.vector(rt$V2);
n_promoters = dim(rt)[1];


if(direction=="R1")
{
promoter_sequence_reverse <- vector(length=n_promoters);
sub_tm1 <- Sys.time();
	for(i in 1:n_promoters){
	        if(substr(promoter_sequence[i],2,2)=="U") {
                next;
        	}
        promoter_sequence_reverse[i] <-as.character(reverseComplement(DNAString(promoter_sequence[i])));
	}
promoter_sequence <- promoter_sequence_reverse;
sub_tm2 <- Sys.time();
sub_tm2 - sub_tm1;
}

n_reads <- countLines(bc_data_file);

#print(n_reads);
read_load_size = 1e6;
n_load = floor((n_reads-1)/read_load_size)+1;

for (i in 1:(n_load) )
{
	n_skip <- read_load_size*(i-1);
	cur_seq_data <- read.table(bc_data_file, skip=n_skip, nrows = read_load_size, sep=",");
	cur_seq_list <- as.vector(cur_seq_data$V2);
	barcode_id_from_reads <- as.vector(cur_seq_data$V5);

	n_reads <- dim(cur_seq_data)[1];
	print(sprintf("starting alignment: %d/%d",i,n_load));
	la <- vector(length=n_reads);
	promoter_start_index <- vector(length=n_reads);
	read_start_index <- vector(length=n_reads);
	do_append = FALSE;

        for (j in 1:n_reads)
        {
        	if(j%%1e4==1)
                {
                	print(sprintf("%d/%d: %2.2f%%",i, n_load, 100*j/n_reads));
                }
 	       barcode_id <- barcode_id_from_reads[j];
        	la_temp <- pairwiseAlignment( substr(cur_seq_list[j],read_start_position, nchar(cur_seq_list[j])) , promoter_sequence[ barcode_id ], type="local");
		la[j] <- score(la_temp);
		promoter_start_index[j] <- parse_alignment_start_index_subject(la_temp);
		read_start_index[j] <-  parse_alignment_start_index_pattern(la_temp);
        }
	cur_seq_data$V7 = la;
	cur_seq_data$V8 = la>35;
	cur_seq_data$V9 = promoter_start_index;
	cur_seq_data$V10 = read_start_index;
	write.table(cur_seq_data, output_file, sep=",", append=do_append, row.names=FALSE, col.names=FALSE);
	rm(cur_seq_data);
	do_append = TRUE;
}
return (la);
}
#test if test_R1_data can align to promoter sequence.

#test if test_R2_data can align to promoter sequence.
