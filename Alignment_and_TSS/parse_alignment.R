#parse_alignment.R
#Functions to parse output of pairwiseAlignment. 
#parse_alignemnt_start_index: 
#	It parses output of pairwiseAlignment to obtain score and alignment start site.

parse_alignment_start_index_list <- function( pairwiseAligment_output)
{
	o = list();
	p<- pattern(pairwiseAligment_output);
	o$pattern_start <- attr(attributes(p)$range,"start");

	s <- subject(pairwiseAligment_output);
	o$subject_start <- attr(attributes(s)$range,"start");

	return (o);
}

parse_alignment_start_index_pattern <- function( pairwiseAligment_output)
{
	p <- pattern(pairwiseAligment_output);
	p_start <- attr(attributes(p)$range,"start");
	return(p_start);
}

parse_alignment_start_index_subject <- function( pairwiseAligment_output)
{
	s <- subject(pairwiseAligment_output);
	s_start <- attr(attributes(s)$range,"start");
	return(s_start);
}
