import os
import subprocess


def run_kmer_sh_file(dna_sequence_path, dsk_results_path):

    s = subprocess.Popen(args=["/usr/src/app/dsk/bin/kmer.sh %s %s" %
                               (dna_sequence_path, dsk_results_path)], shell=True)
    print("done")
