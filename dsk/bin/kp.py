import os
from subprocess import Popen, PIPE, STDOUT
import subprocess


def run_kmer_sh_file(dna_sequence_path, dsk_results_path):

    command = ["bash", "dsk/bin/kmer.sh",
               dna_sequence_path, dsk_results_path]
    try:
        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        output = process.stdout.read()
        exitstatus = process.poll()
        print(output)
    except Exception as e:
        print(str(e))
