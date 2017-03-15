import pysam
import sys
from collections import defaultdict

def write_reference(align):
	fh = open('references/' + align.reference_name.replace('|','_') + '.fasta', 'w')
	fh.write(">%s\n%s\n" % (align.reference_name, align.get_reference_sequence()))
	fh.close()

def checkalign(alignment, args):
	if alignment.is_unmapped:
		return 0

	if args.min_length:
		if alignment.reference_length < args.min_length:
			return 0

	if args.max_length:
		if alignment.reference_length > args.max_length:
			return 0
	return 1

def make_clusters(args):
	filecache = {}
	numseqs = defaultdict(int)

	infile = pysam.AlignmentFile(args.bamfile, "rb")
	for s in infile:
		if not checkalign(s, args):
			continue

		numseqs[s.reference_name] += 1

	infile = pysam.AlignmentFile(args.bamfile, "rb")
	for s in infile:
		if not checkalign(s, args):
			continue

		if numseqs[s.reference_name] > args.min_reads:
			if s.reference_name not in filecache:
				filecache[s.reference_name] = open('clusters/' + s.reference_name + '.cluster.fasta', 'w')
				write_reference(s)

			filecache[s.reference_name].write(">" + s.query_name + "\n" + s.query + "\n")

	for k, v in numseqs.iteritems():
		print "%s\t%s" % (k, v)

import argparse

parser = argparse.ArgumentParser(description='Parse SAM/BAM file into reference clusters.')
parser.add_argument('--min-length', dest='min_length', type=int, help='minimum length of the alignment')
parser.add_argument('--max-length', dest='max_length', type=int, help='maximum length of the alignment')
parser.add_argument('bamfile', type=str, help='sam/bam file')
parser.add_argument('min_reads', type=int, help='minimum number of reads to form a cluster')

args = parser.parse_args()
print args
make_clusters(args)
