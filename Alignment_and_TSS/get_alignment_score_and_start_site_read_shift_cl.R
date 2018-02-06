#Run TSS call from command line
#
#Usage: `Rscript get_alignment_score_and_start_site_read_shift_cl ANTHONY_R2_FILENAME`;
#
#Output file will be same name as ANTHONY_R2_FILENAME added of a suffix `TSScall.txt`.

source("get_alignment_score_and_start_site_read_shift.R");

args <- commandArgs(trailingOnly = T);

bc_data_file=args[1]; #"/Users/gomesa/projects/hpt/library/2Nathan/readtest/testouput2"; #args[1];
promoter_sequence_file = "promoter_plus_ATG_plus_barcode.txt";
direction="R2";
output_file=sprintf("%s_TSScall.txt",bc_data_file);

x=get_alignment_score_and_TSS(bc_data_file, promoter_sequence_file, direction, output_file, read_start_position=3);
  



