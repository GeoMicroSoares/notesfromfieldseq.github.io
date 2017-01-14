import csv
import sys

accessions = set()

tsvfile = sys.argv[1]
accessionlookupfile = sys.argv[2]

reader = csv.DictReader(open(tsvfile), dialect='excel-tab', quoting=csv.QUOTE_NONE)
for row in reader:
	if row['genbank_accession']:
		accessions.add(row['genbank_accession'].strip())

lookup = csv.DictReader(open(accessionlookupfile), dialect='excel-tab')
lookuptable = dict([(row['accession'], (row['taxid'], row['gi'])) for row in lookup if row['accession'] in accessions])

reader = csv.DictReader(open(tsvfile), dialect='excel-tab', quoting=csv.QUOTE_NONE)
for row in reader:
	for k in row.keys():
		if row[k]:
			row[k] = row[k].strip()

	if row['subspecies_taxID']:
		taxID = row['subspecies_taxID']
	elif row['species_taxID']:
		taxID = row['species_taxID']
	elif row['genus_taxID']:
		taxID = row['genus_taxID']
	elif row['family_taxID']:
		taxID = row['family_taxID']
	elif row['order_taxID']:
		taxID = row['order_taxID']
	elif row['class_taxID']:
		taxID = row['class_taxID']
	elif row['phylum_taxID']:
		taxID = row['phylum_taxID']
	else:
		print >>sys.stderr, "No taxID"
		taxID = 0

	if not row['nucleotides']:
		continue

	acc = row['genbank_accession']
	if not acc:
		continue

	if acc not in lookuptable:
		print >>sys.stderr, "%s not in lookuptable" % (acc)
		continue

	rec = ">%s|%s-%s-%s-%s|%s|%s|kraken:taxid|%s|gi|%s\n%s" % (row['recordID'], row['class_name'], row['order_name'], row['family_name'], row['genus_name'], row['species_name'].replace(' ', '_'), acc, lookuptable[acc][0], lookuptable[acc][1], row['nucleotides'].replace('-', '').replace(' ', ''))
	print rec.encode('ascii', 'ignore')


