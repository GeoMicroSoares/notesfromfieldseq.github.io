#!/bin/bash -x

db=$1
fasta=$2
sampletag=$3

#nanopolish extract $dir > $fasta
bwa mem -x ont2d -t 8 db/"$db".fasta $fasta | samtools view -bS - | samtools sort - -o $sampletag.sorted.bam

python scripts/bam_to_clusters.py --min-length 1350 $sampletag $sampletag.sorted.bam 10 | sort -nr -k2 > "$sampletag".clusters.txt

#for fn in references/*.fasta;
#do
#    clusterfn=${fn/references/clusters}
#    clusterfn=${clusterfn/fasta/cluster.fasta}
#    bwa index $fn
#    bwa mem -x ont2d -t 8 $fn $clusterfn | samtools view -bS - | samtools sort - -o "$clusterfn".sorted.bam
#    samtools index "$clusterfn".sorted.bam
#done

