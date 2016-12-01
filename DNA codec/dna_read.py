""" Decodes a DNA string into a file according to a given codebook.

The DNA string is expected to be error free; if there are errors, first correct these, then run this file.

Author: Azat Akhmetov <azat@utexas.edu>
"""
import math
import pickle
import time

import codebook_utilities

# Inputs and parameters
dna_filename = "Input/Encoded DNA/Hamming 10 kb encoded dna.txt"
output_file = "Output/tars/Hamming 10 kb decoded.tar"

reverse_codebook_path = 'Input/reverse codebook.pickle'  # A pickle file which maps numbers to codebook. Should correspond to the codebook used for encoding.

need_to_decompress = True  # If true, will attempt to decompress data with LZMA after decoding. Correct value depends on whether you compressed when encoding.
decoded_bytes_path = 'Intermediate data/decoded bytes.txt'  # A dump of the input as a bytestream, for debug


# Load the DNA-number conversion table
codebook = pickle.load(open(reverse_codebook_path, 'rb'))


# Determine block length of the coding scheme from the first codeword
block_size = codebook_utilities.determine_block_size(list(codebook.keys()))


# Read DNA string, and convert according to codebook
encoded_dna = open(dna_filename).read()

decoded_number = []
for i in range(0, len(encoded_dna), block_size):
    block = encoded_dna[i:i+block_size]

    value = codebook[block]
    decoded_number += [value]


# Convert a base-n number into a byte array
def base_n_to_byte_array(digits, from_base):
    """ Converts a base n number to a byte array.

    :param digits: Digits of the number, starting from highest.
    :param from_base: Base in which the number is given.
    """

    x = 0
    n = len(digits)

    now = time.time()
    print('Beginning conversion of {0} digits to bytes...'.format(len(digits)))
    for i in range(0, len(digits)):
        x += digits[i] * (from_base ** (n-i-1))

        # Progress report
        new_now = time.time()
        if new_now-now > 1:
            print('{0:.1%} complete...'.format(i/len(digits)))
            now = new_now

    min_length = max(math.ceil(math.log(x, 256)), 1)
    byte_array = x.to_bytes(min_length, byteorder='big')

    print('Finished converting.')
    return byte_array


decoded_bytes = base_n_to_byte_array(decoded_number, len(codebook))
open(decoded_bytes_path, 'w').write('\n'.join([str(b) for b in decoded_bytes]))


# Decompress
if need_to_decompress:
    import lzma

    print("Decompressing file with LZMA...")
    decompressed_file = lzma.decompress(data=decoded_bytes, format=lzma.FORMAT_XZ)
else:
    decompressed_file = decoded_bytes


# Save to file
open(output_file, 'wb').write(decompressed_file)
