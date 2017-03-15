from Bio import SeqIO
import sys

SeqIO.write(SeqIO.parse(open(sys.argv[1]), "genbank"), sys.stdout, "fasta")
