#!/bin/bash

db=$1
dir=$2
sampletag=$3

nanopolish extract $dir > $sampletag.fasta
bwa mem -x ont2d -t 8 /metabarcoding/notesfromfieldseq.github.io/db/"$db".fasta $sampletag.fasta | samtools view -bS - | samtools sort - -o $sampletag.sorted.bam

# make this an outdirectory thing
mkdir -p clusters
mkdir -p references

python /metabarcoding/notesfromfieldseq.github.io/scripts/bam_to_clusters.py --min-length 1350 --max-length 1550  $sampletag.sorted.bam 50 | sort -nr -k2

for fn in references/*.fasta;
do
    clusterfn=${fn/references/clusters}
    clusterfn=${clusterfn/fasta/cluster.fasta}
    bwa index $fn
    bwa mem -x ont2d -t 60 $fn $clusterfn | samtools view -bS - | samtools sort - -o "$clusterfn".sorted.bam
    samtools index "$clusterfn".sorted.bam
done

