"""Batch-clean mutated DNA by calling the error correction function on every single file.

This is glue code to facilitate batch processing of many input files. The actual logic is in another file (clean_dna.py,
referenced from here).

Author: Azat Akhmetov <azat@utexas.edu>
"""
import clean_dna
import os


# Inputs
mutated_dna_path = os.path.join('Input', 'Mutated DNA')  # Files are expected to be nested in folders under this path, eg. Input/Mutated DNA/run 1/mutated dna file.txt
cleaned_dna_path = os.path.join('Output', 'Cleaned DNA')
codewords_path = os.path.join('Input', 'codewords.txt')  # Text list of codewords


# Get list of subfolders (these are typically replicate runs)
for d in os.listdir(mutated_dna_path):
    this_path = os.path.join(mutated_dna_path, d)
    print('Now doing {}'.format(this_path))

    for f in os.listdir(this_path):
        input_dna_filename = os.path.join(this_path, f)

        output_dna_path = os.path.join(cleaned_dna_path, d)
        if not os.path.exists(output_dna_path): os.makedirs(output_dna_path)
        output_dna_filename = os.path.join(output_dna_path, f.replace('mutated', 'cleaned'))

        clean_dna.clean_dna(input_dna_filename, output_dna_filename, codewords_path)
