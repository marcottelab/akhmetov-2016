"""Takes a list of codewords and constructs a codebook (and a reverse codebook) and stores it as a python pickle file.

The difference is that a codeword list is just a list of sequences, while a codebook has the sequences with correspon-
ding numerical values.

Author: Azat Akhmetov <azat@utexas.edu>
"""

import pickle


# Inputs and parameters
codeword_list_file = 'Input/codewords.txt'
codebook_file = 'Output/Codebook/codebook.pickle'
reverse_codebook_file = 'Output/Codebook/reverse codebook.pickle'


def main():
    # Load the codeword list
    codewords = open(codeword_list_file, 'r').read().splitlines()

    # Construct codebook by mapping each codeword to a value
    codebook = {}
    reverse_codebook = {}
    for i in range(len(codewords)):
        codebook[i] = codewords[i]
        reverse_codebook[codewords[i]] = i

    # Save codebooks to file
    pickle.dump(codebook, open(codebook_file, 'wb'))
    pickle.dump(reverse_codebook, open(reverse_codebook_file, 'wb'))


main()
