""" Converts a binary file into a DNA string according to a given bytewise codebook.

Author: Azat Akhmetov <azat@utexas.edu>
"""
import math
import pickle
import time


# Inputs and parameters
input_file = 'Input/tars/Hamming 10 kb.tar'

encoded_dna_filename = 'Output/Encoded DNA/Hamming 10 kb encoded dna.txt'
encoded_blocks_filename = 'Output/Encoded DNA/Hamming 10 kb encoded blocks.txt'

codebook_path = 'Input/codebook.pickle'  # A pickle file generated by construct_codebooks.py which maps each codeword to a number. Do not lose this! It is necessary for decoding.

compress_data = True  # Whether the compress data before encoding. Setting this to false is not recommended, the option is here for debugging.
encoded_bytes_path = 'Intermediate data/encoded bytes.txt'  # A dump of the input as a bytestream, for debug


# Load the codebook DNA-number conversion table
codebook = pickle.load(open(codebook_path, 'rb'))


# Read file as list of bytes and convert into a base-n number (for n codewords)
def bytes_to_base_n(byte_array, to_base):
    """ Converts a byte array to a base n number.

    :param byte_array: Array of bytes, with most significant byte (highest digit) first.
    :param to_base: What base the result should be in.
    :return: The number in the new base, given as array of digits, most significant first.
    """

    x = int.from_bytes(byte_array, byteorder='big')

    result = []
    carry_over = x
    now = time.time()
    print('Beginning conversion of {0} bytes to numbers...'.format(len(byte_array)))
    while carry_over > 0:
        remainder = int(carry_over % to_base)
        result.insert(0, remainder)

        new_carry_over = (carry_over - remainder) // to_base
        carry_over = new_carry_over

        new_now = time.time()
        if new_now-now > 1:
            print('{0:.1%} complete...'.format(1 - math.log(carry_over)/math.log(x)))
            now = new_now

    if len(result) < 1:
        result = [0]

    print('Finished converting.')
    return result


n = len(codebook)

raw_file = open(input_file, 'rb').read()

if compress_data:
    import lzma

    print("Compressing file with LZMA...")
    bytes_to_encode = lzma.compress(data=raw_file, format=lzma.FORMAT_XZ)
else:
    bytes_to_encode = raw_file

open(encoded_bytes_path, 'w').write('\n'.join([str(b) for b in bytes_to_encode]))

converted_to_new_base = bytes_to_base_n(bytes_to_encode, n)


# Encode each digit into DNA
encoded = []
for d in converted_to_new_base:
    w = codebook[d]
    encoded += [w]


# Write DNA sequence to files
encoded_blocks = '\n'.join(encoded)
open(encoded_blocks_filename, 'w').write(encoded_blocks)

encoded_dna = ''.join(encoded)
open(encoded_dna_filename, 'w').write(encoded_dna)

print('Done!')
