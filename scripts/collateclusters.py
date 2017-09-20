import sys
from Bio import SeqIO
import glob
import os.path
from collections import defaultdict

lookup = {}

for rec in SeqIO.parse(open(sys.argv[1]), "fasta"):
	lookup[rec.id] = rec.description

results = defaultdict(list)

for sample in sys.argv[2:]:
	for fn in glob.glob(sample + '/clusters/*.cluster.fasta'):
		refid = os.path.basename(fn)

		hits = len(list(SeqIO.parse(open(fn), 'fasta')))

		tofind = refid.replace('.cluster.fasta', '')

		results[sample].append((hits, lookup[tofind]))


for sample, hits in results.iteritems():
	total_hits = sum([h[0] for h in hits])

	for h in hits:
		taxonomy = h[1].split(" ")

		print "%s\t%s\t%s %s\t%s\t%s\t%s" % (sample, taxonomy[1], taxonomy[1], taxonomy[2], h[1], h[0], h[0]/float(total_hits))

