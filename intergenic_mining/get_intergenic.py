## Nathan Johns 2017
## Requires full genbank file with genome sequence
## Usage: python get_intergenic.py genbank_filename minsize
## Example: python get_intergenic.py Test.gb 200

import sys
from Bio import SeqIO

gb_file = open(sys.argv[1]) #Genbank file to parse
minsize = int(sys.argv[2])      #Minimum size of intergenic region

# Iterate through genbank features and collect coordinates, strands
def parse_regions(gb_file):
	gene_ids = []
	gene_coordinates = {}
	gene_dna = {}
	for record in SeqIO.parse(gb_file, "gb"):
		genome = record.seq
		for features in record.features:
			if features.type == 'gene':
				try:
					product = features.qualifiers['locus_tag'][0]
					gene_ids.append(product)
					loc = str(features.location)
					coordinates = parse_coordinates(loc)
					gene_coordinates[product]=coordinates
					if len(gene_coordinates) != len(gene_ids):
						sys.exit()
				except KeyError:
					pass
			if len(gene_coordinates.keys()) != len(gene_ids):
				print 'The list of genes coordinates != list of genes'
				print 'exiting'
				sys.exit()

# Get gene DNA sequences
	for keys in gene_coordinates:
		gene_dna[keys] = genome[int(gene_coordinates[keys][0]):int(gene_coordinates[keys][1])]
# Reverse complement gene sequences on minus strand
		if gene_coordinates[keys][2] == '-':
			gene_dna[keys] = gene_dna[keys].reverse_complement()
	return genome, gene_coordinates, gene_ids

# Take string coordinate and output as list with start, end, strand
def parse_coordinates(loc):
	replace = ['[',']','(',')','<','>','+','-']
	if '+' in loc:
		strand = '+'
	if '-' in loc:
		strand = '-'
	elif '-' not in loc and '+' not in loc:
		strand = 'Not Available'
	for ch in replace:
		loc = loc.replace(ch,'')
	coordinates = loc.split(':')
	coordinates.append(strand)
	return coordinates

# Write intergenic sequences in fasta format
def write_intergenic_fasta(minsize,gene_coordinates,gene_ids,genome):
	ign_outputfile = open(sys.argv[1][:-3]+'_ign.fasta','w')
	starts = []
	ends = []
	strands = []
	for g in gene_ids:
		starts.append(gene_coordinates[g][0])
		ends.append(gene_coordinates[g][1])
		strands.append(gene_coordinates[g][2])

	for i in range(0,len(starts)):
		try:
			igr_seq = genome[int(ends[i]):int(starts[i+1])]
			if len(igr_seq) >= minsize and int(ends[i]) < int(starts[i+1]):
				header = ' '.join(['>',gene_ids[i],gene_ids[i+1],strands[i]+strands[i+1],'\n'])
				ign_outputfile.write(header)
				ign_outputfile.write(str(igr_seq)+'\n\n')
# If IndexError is from first gene feature, write seq between end of final gene
# and beginning of first gene. Otherwise pass.
		except IndexError:
			if i ==1:
				igr_seq = str(genome[int(ends[len(starts)]):])+str(genome[:starts[1]])
				if len(igr_seq) >= minsize:
					ign_outputfile.write(' '.join(['>',gene_ids[i],gene_ids[-1],strands[i]+strands[-1],'\n']))
					ign_outputfile.write(str(igr_seq)+'\n\n')
			else:
				pass

def main():
	genome, gene_coordinates, gene_ids = parse_regions(gb_file)
	write_intergenic_fasta(minsize,gene_coordinates,gene_ids,genome)

main()
