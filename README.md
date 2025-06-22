
This repository contains barcode files, and script to build them, to be used with the lineage typing tool [fastlin](https://github.com/rderelle/fastlin).

# MTBC barcode files 

###  MTBC_barcodes_v1.tsv
This file contains 1,100 MTBC SNP barcodes that were built, tested, and used in the Bioinformatics manuscript describing fastlin. These barcodes were extracted from TB-profiler v5.0.0, with the exception of the SNP at position 1,882,572 (lineage 4.9.1), which was excluded because it appeared in every sample when using k=25.

###  MTBC_barcodes_v2.tsv
This file contains an updated in-house set of 1,220 SNP barcodes, based on TB-profiler v6.6.2, with the following modifications:
- removed the SNP at position 1,882,572 (as above), and all SNP barcodes corresponding to M. canetti, which were mostly not detected by fastlin.
- added 10 new SNP barcodes each for the <i>species</i> M. canetti, M. microti, and M. pinnipedii.
- supplemented barcodes for La(x) lineages, which previously had only 4–5 barcodes; all but two now have 10 SNP barcodes.

The performance of these barcodes on 729 MTBC genome assemblies is shown in the file out_fastlin_v2.txt.

###  MTBC_barcodes_v3.tsv
This file contains 1,230 SNP barcodes derived from v2:
- reverse-complemented some barcodes of v2. This has no impact on fastlin inferences but allows to generate the barcode file using the script data/1_build_barcode_file.py and the SNP file data/SNP_file_v3.tsv.
- added 10 new SNP barcodes for lineage 10

The performance of these barcodes on 729 MTBC genome assemblies is shown in the file out_fastlin_v3.txt.

# build your own barcode file
To build your own barcode file, you will need:
+ python 3+
+ the genome assembly of M. tuberculosis (used to identify the SNPs)
+ a tab-delimited SNP file

The tab-delimited SNP file should have 3 columns: (i) the lineage, (ii) 0-based positions of the SNPs in the genome assembly and (iii) the alternative nucleotide corresponding to the SNP. The script '1_build_barcode_file.py' generates the barcode file as output ('output.tsv').

An example of input files is provided in the directory 'data' (you will need first to uncompress the fasta file):
```
python3 1_build_barcode_file.py -g data/H37Rv_genome.fasta -s data/SNPs_file_v3.tsv
```

Once the barcode file has been generated, you can use the script '2_test_barcode_file.py' to test a range of kmer sizes (here from 11 to 99) in order to determine the minimal kmer size at which fastlin would not generate false positives.
The script takes as input the barcode file, a genome assembly file for which the lineage is known and the lineage of the genome assembly (the script will ignore all barcodes corresponding to this lineage):
```
python3 2_test_barcode_file.py -g data/H37Rv_genome.fasta -b MTBC_barcodes_v3.tsv -l 4.9
```







