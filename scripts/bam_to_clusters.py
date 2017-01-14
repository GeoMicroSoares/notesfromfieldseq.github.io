import pysam
import sys
from collections import defaultdict

THRESHOLD = 100

def write_reference(align):
	fh = open('references/' + align.reference_name.replace('|','_') + '.fasta', 'w')
	fh.write(">%s\n%s\n" % (align.reference_name, align.get_reference_sequence()))
	fh.close()

filecache = {}
numseqs = defaultdict(int)

infile = pysam.AlignmentFile(sys.argv[1], "rb")
for s in infile:
	if s.is_unmapped:
		continue

	numseqs[s.reference_name] += 1

infile = pysam.AlignmentFile(sys.argv[1], "rb")
for s in infile:
	if s.is_unmapped:
		continue

	if numseqs[s.reference_name] > THRESHOLD:
		if s.reference_name not in filecache:
			filecache[s.reference_name] = open('clusters/' + s.reference_name + '.cluster.fasta', 'w')
			write_reference(s)

		filecache[s.reference_name].write(">" + s.query_name + "\n" + s.query + "\n")

for k, v in numseqs.iteritems():
	print "%s\t%s" % (k, v)
