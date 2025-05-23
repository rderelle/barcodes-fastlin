# barcodes-fastlin

This repository contains barcode files, and script to build them, to be used with the lineage typing tool [fastlin](https://github.com/rderelle/fastlin).

### file 'MTBC_barcodes.tsv'
This file contains all MTBC SNP barcodes built, tested and used in the Bioinformatics manuscript describing fastlin.

### build your own barcode file
To build your own barcode file, you will need:
+ python 3+
+ the genome assembly of M. tuberculosis (used to identify the SNPs)
+ a tab-delimited SNP file

The tab-delimited SNP file should have 3 columns: (i) the lineage, (ii) 0-based positions of the SNPs in the genome assembly and (iii) the alternative nucleotide corresponding to the SNP. The script '1_build_barcode_file.py' generates the barcode file as output ('output.tsv').

An example of input files is provided in the directory 'data' (you will need first to uncompress the fasta file):
```
python3 1_build_barcode_file.py -g data/H37Rv_genome.fasta -s data/SNPs_file.tsv
```

### test your barcode file
Once the barcode file has been generated, you can use the script '2_test_barcode_file.py' to test a range of kmer sizes (here from 11 to 99) in order to determine the minimal kmer size at which fastlin would not generate false positives.
The script takes as input the barcode file, a genome assembly file for which the lineage is known and the lineage of the genome assembly (the script will ignore all barcodes corresponding to this lineage):
```
python3 2_test_barcode_file.py -g data/H37Rv_genome.fasta -b MTBC_barcodes.tsv -l 4.9
```







