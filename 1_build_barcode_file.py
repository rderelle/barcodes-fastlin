import os
import csv
import collections
import argparse
import sys


def parse_args():
    # define and parse command-line arguments
    parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter, epilog=' \n')
    common = parser.add_argument_group()
    common.add_argument('-g', help='fasta genome file [required]', metavar='')    
    common.add_argument('-s', help='tab-delimited SNP barcodes [required]', metavar='')    
    common.add_argument('-h', action="help", help="show this help message and exit")
    args = parser.parse_args()
    
    if not args.g :
        sys.exit('\n            ERROR: please specify a fasta genome file\n\n')
    elif not args.s :
        sys.exit('\n            ERROR: please specify a tab-delimited SNP barcodes\n\n')
    
    return args.g, args.s


def read_fasta(fasta_content):
    name, seq = None, []
    for line in fasta_content:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name.replace('>',''), ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name.replace('>',''), ''.join(seq))




if __name__ == "__main__":
    
    # get arguments
    genome_file, SNP_file = parse_args()
    

    # size of left and right kmers
    kmer_size = 50
    
    
    # create output file
    output = open('output.tsv', 'w+')
    
    
    # get reference genome
    ref_genome = ''
    with open(genome_file) as fasta_content:
        for name, seq in read_fasta(fasta_content):
            ref_genome += seq
    
    
    # write genome size
    output.write('genome_size	' + str(len(ref_genome)) + '\n')
    
    
    # extract and write SNP barcodes
    file_content = csv.reader(open(SNP_file), delimiter='	')
    for line in file_content:
        # extract info
        lineage = line[0]
        pos_0_based = int(line[1])
        alt_nucl = line[2]
        
        # build left and right kmers
        left_kmer  = ref_genome[pos_0_based - kmer_size : pos_0_based]
        right_kmer = ref_genome[pos_0_based + 1 : pos_0_based + 1 + kmer_size]
        
        # save it
        output.write(lineage + '	' + left_kmer + '	' + alt_nucl + '	' + right_kmer + '\n')

    output.close()


        
    
