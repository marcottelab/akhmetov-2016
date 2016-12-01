""" Simulates mutations in a DNA sequence.

Author: Azat Akhmetov <azat@utexas.edu>
"""


import random
import os
import numpy
import math


# Inputs
data_points = 50
lowest = 0.0001
highest = 0.5

input_filename = 'Input/DNA to be mutated/Hamming 10 kb encoded dna.txt'
output_directory = 'Output/Mutated DNA/'

runs = 10  # Number of times to repeat the experiment; they will be in folders called run 1, run 2, etc

nucleotides = ['A', 'C', 'G', 'T']


# Calculate the log-spaced mutation rate array
lowest_exp = math.log(lowest)
highest_exp = math.log(highest)

mutation_rates = [x for x in numpy.logspace(lowest_exp, highest_exp, num=data_points, base=math.e)]

# Load input DNA and mutate randomly
input_dna = list(open(input_filename).read())
length_of_input_dna = len(input_dna)


for run in range(1, runs+1):
    print('Mutating run {}:'.format(run))
    for mut_rate in mutation_rates:
        number_of_mutations = int(round(length_of_input_dna * mut_rate))
        f = '{:2.6f} muts per bp mutated.txt'.format(mut_rate)
        print('\t{} with {} mutations'.format(f, number_of_mutations))

        output_dna = list(input_dna)  # Needs to call list to copy vs. just point them both to the same thing
        for i in range(0, number_of_mutations):
            j = random.randint(0, length_of_input_dna - 1)

            choices = [n for n in nucleotides if n != output_dna[j]]
            output_dna[j] = random.choice(choices)

        d = os.path.join(output_directory, 'run {}'.format(run))
        if not os.path.exists(d): os.makedirs(d)
        open(os.path.join(d, f), 'w').write(''.join(output_dna))
