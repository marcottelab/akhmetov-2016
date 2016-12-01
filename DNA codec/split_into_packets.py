"""Splits a single long sequence of DNA into short, overlapping segments (packets).

Author: Azat Akhmetov <azat@utexas.edu>
"""
import math


# Parameters and constants
packet_length = 200  # Desired length of each packet
step = 25  # How much to move the window by in each iteration, packet_length-step will be the overlap between two successive packets

encoded_dna_filename = 'Input/Encoded DNA/Hamming 10 kb encoded dna.txt'
output_filename = 'Output/Packets/Hamming 10 kb packets.txt'


# Program logic below
full_dna = open(encoded_dna_filename).read()

position = 0 - packet_length + step
packets = []
while position < len(full_dna) - step:
    i = max(0, position)
    j = min(len(full_dna), position + packet_length)

    packets += [full_dna[i:j]]
    position += step

# Write to file
open(output_filename, 'w').close()

with open(output_filename, 'a') as f:
    n_packets = len(packets)
    n_digits = math.ceil(math.log10(n_packets+1))
    for i in range(0, n_packets):
        name = '>Piece_' + str(i).zfill(n_digits)
        f.write(name + '\n' + packets[i] + '\n\n')
