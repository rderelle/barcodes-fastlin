import sys
import os
import csv
import gzip
import collections
import argparse


def parse_args():
    # define and parse command-line arguments
    parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter, epilog=' \n')
    common = parser.add_argument_group()
    common.add_argument('-g', help='fasta genome file [required]', metavar='')    
    common.add_argument('-b', help='barcode file [required]', metavar='')    
    common.add_argument('-l', help='lineage of genome assembly [required]', metavar='')    
    common.add_argument('-h', action="help", help="show this help message and exit")
    args = parser.parse_args()
    
    '''
    if not args.g :
        sys.exit('\n            ERROR: please specify a fasta genome file\n\n')
    elif not args.l :
        sys.exit('\n            ERROR: please specify a the lineage corresponding to this genome\n\n')
    elif not args.b :
        sys.exit('\n            ERROR: please specify a barcode file\n\n')
    '''
    return args.g, args.b, args.l



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


def reverse_complement(st):
    nn = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    return "".join(nn[n] for n in reversed(st))


def get_ref_barcodes(barcode_file, s_sublineage, half_k_size):
    all_lineages = set()
    all_nucl = ['A','T','G','C']
    d_kmer_2_lineage = dict()
    counter = 0
    file_content = csv.reader(open(barcode_file), delimiter='	')
    for line in file_content: 
        if line[0] != 'genome_size':
            counter += 1
            lineage = line[0]
            all_lineages.add(lineage)
        
            if not lineage in s_sublineage:
                id_kmer = lineage + '__' + str(counter)
        
                kmer_left = line[1][-1 * half_k_size :]
                middle_base = line[2]        
                kmer_right = line[3][: half_k_size]
       
                kmer_seq = kmer_left + middle_base + kmer_right 
                d_kmer_2_lineage[kmer_seq] = id_kmer
        
                rc_kmer = reverse_complement(kmer_seq)
                d_kmer_2_lineage[rc_kmer] = id_kmer

    return d_kmer_2_lineage




if __name__ == "__main__":

    # get arguments
    genome_file, barcode_file, lineage = parse_args()

    
    # loop over kmer sizes
    print('#kmer_size	false_positive')
    for kmer_size in range(11,100):
        
        if kmer_size % 2 != 0:

            # get half kmer size
            half_kmer_size = int(round((kmer_size -1) /2))
            
            
            # extract sub-lineages
            sublineages = set()
            l_lineages = lineage.split('.')
            for n in range(len(l_lineages)):
                sub = '.'.join(l_lineages[:n + 1])
                sublineages.add(sub)

            
            # get reference barcodes
            barcode_kmers = get_ref_barcodes(barcode_file, sublineages, half_kmer_size)
            
            
            # test all kmer from the genome
            s_false_positives = set()
            with open(genome_file) as fasta_content:
                for name, seq in read_fasta(fasta_content):
                    for n in range(len(seq) - kmer_size +1):
                        kmer = seq[n:n + kmer_size] 
                        rc_kmer = reverse_complement(kmer)
                        
                        if kmer in barcode_kmers:
                            id_kmer = barcode_kmers[kmer]
                            s_false_positives.add(id_kmer)
                        
                        elif rc_kmer in barcode_kmers:
                            id_kmer = barcode_kmers[rc_kmer]
                            s_false_positives.add(id_kmer)


            if len(s_false_positives) > 10:
                 print(str(kmer_size) + '	' + str(len(s_false_positives)))
            else:
                 print(str(kmer_size) + '	' + str(len(s_false_positives)) + '	' + ','.join(x for x in s_false_positives))
        
        






