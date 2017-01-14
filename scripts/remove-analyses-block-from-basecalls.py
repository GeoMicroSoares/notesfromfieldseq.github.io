
import h5py
import os
import sys

if len(sys.argv) != 2:
	print "Usage: remove-analyses-block-from-fast5.py <directory to recurse>"
	raise SystemExit

count = 0
for root, dirs, files in os.walk(sys.argv[1]):
	for fn in files:
		if fn.endswith('.fast5'):
			filepath = root + '/' + fn
			fh = h5py.File(filepath, 'r+')
			if 'Analyses' in fh:
				del fh['Analyses']
				count += 1
			fh.close()

print >>sys.stderr, "Removed %d analyses blocks" % (count)
