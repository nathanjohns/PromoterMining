# PromoterMining

Code and materials from paper **"Metagenomic mining of regulatory elements enables programmable species-selective gene expression"**
Nathan I. Johns*, Antonio L.C. Gomes*, Sung Sun Yim, Anthony Yang, Tomasz Blazejewski, Christopher S. Smillie, Mark B. Smith, Eric J. Alm, Sriram Kosuri, Harris H. Wang
*Nature Methods* (2018)
*Denotes equal contribution

Supplemental information: (insert link when published)

Protocol Exchange: (insert link when published)

## Dependencies
The following must be installed prior to executing the code in this repository. For Python packages, it may be convenient to obtain these through a distribution such as [Anaconda](https://www.continuum.io/downloads). Installation should only take a few minutes.
* Python 2.7.X (Jupyter, biopython, pandas, numpy, scipy) 
* R version 3.0.2 or above (Biostrings)

We have tested this code on Mac OS X 10.13.2

## Intergenic region mining
Requires a full genbank file for a genome of interest containing the entire sequence. Move genbank file to intergenic_mining directory. An example execution of the code using a test genome for B. thetaiotaomicron and a minimum intergenic region size of 200 bp is shown below. 
```
$ python get_intergenic.py Test.gb 200
```
The output is a new file in fasta format (example of one intergenic region below). Each header includes the locus name of left gene, name of right gene, strand of left gene, and strand of right gene. 

```
> BT_0010 BT_0011 ++ 
ACAAGAAACGAAACCGGATAAGAAGCCCATGCGGATGGTAACATCCAAGATGAGCATTGAAGAAACTATTGAGGTGCTT
CGCGAGGATCTTAAGACTAATGTACGTTCCAAAGCATGAAGAAAGCATATCCTGCTGAATCCGAAGGTGGAGGGAATGG
CCAGATTCCCGTCCGGGGTTGATTCTGTTTTAATCAACACTCCCGTA
```

## Read Analysis
Move R1 and R2 files to barcode_calling folder For Read 1 and 2 fastq files execute barcode.py by executing the python script as shown below. The same code can be used for RNA and DNA read files. 
```
$ mkdir out
$ python barcode.py example_R1.fastq out/outputfilename_r1.txt 1 r1
$ python barcode.py example_R2.fastq out/outputfilename_r2.txt 1 r2
```
Using the output from the previous code, align R2 reads to reference sequences by executing the following R script using the code below. This is the longest step to execute and takes ~10hr/10^6 reads. Parallelization can speed this step up greatly.
```
$ Rscript get_alignment_score_and_start_site_read_shift_cl.R ../scripts_for_barcode_calling/out/outputfilename_r2.txt 
```
The output file of this script contains the suffix `_TSScall.txt`. In this case, outputfilename_r2_TSScall.txt

Compute TSS_distribution.txt file from previous output by performing the following command line operation:

```
$ awk -F "," '{A[$5" "$9]++; T[$5]++; t[$5" “$9]=$5;} END{for(i in A) print i, A[i], T[t[i]]}’ ../scripts_for_barcode_calling/out/outputfilename_r2.txt_TSScall.txt | sort -n > TSS_distribution.txt
```

Estimate TSS locations by executing the code below using an example file of TSS read start positions for each construct (TSS_distribution_sample.txt). 

```
$ Rscript TSS_point_estimation_by_k-means_Optimize_Ncluster_from_cl.R TSS_distribution_sample.txt
```

## FACS-seq read analysis
First, concatenate counts for each library member into one file following the example of BinCountsExample.csv.

Next, fill in the values for the lists CellCounts and BinFluorescenceValues in the file CalcProtein.py to such that they contain the number of sorted cells and mean fluorescence values for each bin. For example:
```
CellCounts = [3000000,500000,400000,200000,150000,40000,10000,2000]
BinFluorescenceValues = [100,350,500,800,1200,3000,10000,40000]
```

Then, calculate protein values using by executing the following code:
```
$ python CalcProtein.py BinCountsExample.csv
```

## Updates
...
