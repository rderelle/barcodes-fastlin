# barcodes-fastlin

This repository contains barcode files, and script to build them, to be used with the lineage typing tool [fastlin](https://github.com/rderelle/fastlin).

### file 'MTBC_barcodes.tsv'
This file contains all MTBC SNP barcodes built, tested and used in REFERENCE.

### build your own barcode file
To build your own barcode file, you will need:
+ python 3+
+ the genome assembly of M. tuberculosis (used to identify the SNPs)
+ a tab-delimited SNP file

The tab-delimited SNP file should have 3 columns: (i) the lineage, (ii) the 0-based position of the SNP in the genome assembly and (iii) the alternative nucleotide corresponding to the SNP. The script '1_build_barcode_file.py' generates the barcode file as output ('output.tsv').

An example of input files is provided in the directory 'data' (need to uncompress fasta file):
```
python3 1_build_barcode_file.py -g data/H37Rv_genome.fasta -s data/SNPs_file.tsv
```

### test your barcode file




