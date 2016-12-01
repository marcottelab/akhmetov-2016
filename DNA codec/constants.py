"""Various user-specified constants and parameters.

Author: Azat Akhmetov <azat@utexas.edu>
"""

path_to_generated_codeword_list = 'Output/codewords.txt'
path_to_sample_codeword_list = 'Sample input/codewords.txt'
path_to_sample_input_data = 'Sample input/Hamming tiny.7z'

path_to_sample_input_codebook = 'Sample input/codebook.json'
path_to_sample_output_codebook = 'Sample input/codebook.json'

class flags:
    compress = True

class path:
    class input:
        class sample:
            codebook = 'Sample input/codebook.pickle'
            reverse_codebook = 'Sample input/reverse codebook.pickle'

            codeword_list = 'Sample input/codewords.txt'
            dna = 'Sample input/dna.txt'
            dna_concatenated = 'Sample input/encoded dna.txt'
            mutated_dna = 'Sample input/mutated dna.txt'
            cleaned_dna = 'Sample input/cleaned dna.txt'
            nucleotide_map = 'Sample input/Nucleotide map.json'

            uncompressed_tar = 'Sample input/Hamming tiny.tar'

        tar = 'Input/Hamming 10 kb.tar'

        encoded_dna = 'Output/encoded dna Hamming 10 kb.txt'

    class intermediate:
        class coding:
            encoded_bytes = 'Intermediate data/Encoding/encoded bytes.txt'
            decoded_bytes = 'Intermediate data/Encoding/decoded bytes.txt'

    class output:
        codebook = 'Output/codebook.pickle'
        reverse_codebook = 'Output/reverse codebook.pickle'
        data_file = 'Output/data.7z'

        dna_blocks = 'Output/encoded blocks.txt'
        dna_concatenated = 'Output/encoded dna.txt'

        mutated_dna = 'Output/mutated dna.txt'
        #cleaned_dna = 'Output/cleaned dna.txt'
        cleaned_dna = 'Sample input/cleaned dna.txt'

        class packets:
            overlapping = 'Output/dna packets.txt'
