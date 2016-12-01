"""Methods for correcting errors in a single mutated sequence of DNA representing encoded digital data, using the error
correction capacity of the coding scheme.

Author: Azat Akhmetov <azat@utexas.edu>
"""


def clean_dna(mutated_dna_filename, cleaned_dna_filename, codewords_path):
    """ Attempts to correct errors in a DNA sequence.

    Currently only corrects point-mutations. If more than one correction is equally likely, chooses one at random.

    :param codewords_path: Must point to codewords.txt, a text file with one codeword per line.
    """
    import codebook_utilities
    import distance
    import random

    # Load the DNA-number conversion table
    codewords = open(codewords_path).read().splitlines()

    # Determine block length
    block_length = codebook_utilities.determine_block_size(codewords)



    # Load the input DNA
    print('Scanning ' + mutated_dna_filename)

    mutated_dna = open(mutated_dna_filename).read()
    print("\tInput:  " + str(len(mutated_dna)) + " bp DNA")  # extra space so it's aligned with the output message below


    # Go through the input block by block, correcting as you go
    def get_all_hamming_distances(from_word, to_words):
        """ Gets all Hamming distances from a given word to each word in the list.
        """

        distances = []
        for w in to_words:
            d = distance.levenshtein(from_word, w)
            distances += [(w, d)]

        return distances


    clean_dna = ""
    for i in range(0, len(mutated_dna), block_length):
        block = mutated_dna[i:i+block_length]

        distances = get_all_hamming_distances(block, codewords)

        sorted_dist = sorted(distances, key = lambda t: t[1])

        cleaned_block = block
        if sorted_dist[0][1] > 0:
            d = sorted_dist[0][1]
            best_choices = [t for t in distances if t[1] == d]

            if len(best_choices) == 1:
                cleaned_block = best_choices[0][0]
            else:
                cleaned_block = random.choice(best_choices)[0]

        clean_dna += cleaned_block

    print("\tOutput: " + str(len(clean_dna)) + " bp DNA")

    # Save the cleaned DNA to file
    open(cleaned_dna_filename, 'w').write(clean_dna)
