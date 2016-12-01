"""Takes an original DNA sequence as well as its mutated forms, and tries to count how many mutations each one has. The
output is a spreadsheet suitable for importing with R.

Author: Azat Akhmetov <azat@utexas.edu>
"""
import os
import pyexcel
import re


# Inputs
path_to_reference_dna = 'Input/DNA to be mutated/Hamming 10 kb encoded dna.txt'  # Reference sequence that the mutants will be compared to

query_dna_folder = 'Input/Cleaned DNA/'  # Each set of files is expected to be grouped in a folder eg. /Input/Cleaned DNA/run 1
ecc = 'Yes'
report_filename = 'Output/Mutation report cleaned.ods'  # Note: pyexcel uses extension to determine format, I think

data_encoded = 'Hamming.jpg'

# A regex used to extract the mutation rate from your filenames. Must contain a named capturing group:
# (?P<mutation_rate>PATTERN_HERE)
mutation_rate_regex = '(?P<mutation_rate>0.\d+) muts per bp(?: cleaned| mutated)?.txt'


# Load the reference
reference_dna = open(path_to_reference_dna).read().strip()
length_of_reference = len(reference_dna)


# Build a list of input files
results = [['mutations_per_nt', 'percent_bases_correct', 'ecc', 'data_encoded', 'run']]

input_dirs = os.listdir(query_dna_folder)
for d in input_dirs:
    # Get the list of files in this set
    input_files = os.listdir(os.path.join(query_dna_folder, d))

    # Process them one at a time
    for f in input_files:
        print('Now processing ' + f, end='... ')

        rate = re.search(mutation_rate_regex, f).group('mutation_rate')

        s = open(os.path.join(query_dna_folder, d, f)).read().strip()
        if len(s) != length_of_reference:
            print(f + ' doesn\'t have the same length as reference, skipping')
            continue

        matches = sum(1 for t in zip(reference_dna, s) if t[0] == t[1])

        results += [[float(rate), matches/length_of_reference, ecc, data_encoded, d]]

        print('Done!')

# Save the result
pyexcel.save_as(array=results, dest_file_name=report_filename)
