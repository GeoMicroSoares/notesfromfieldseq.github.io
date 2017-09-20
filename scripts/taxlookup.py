import sys
from Bio import SeqIO

tofind = set()

for rec in SeqIO.parse(open(sys.argv[1]), "fasta"):
	tofind.add(rec.id)

for ln in open(sys.argv[2]):
	accession, accver, taxid, gi = ln.split("\t")
	if accver in tofind:
		print "%s\t%s" % (accver, taxid)
