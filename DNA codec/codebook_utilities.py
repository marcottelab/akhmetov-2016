"""Determines the block size of a block-based cipher based on the codebook.

Author: Azat Akhmetov <azat@utexas.edu>
"""


def determine_block_size(codewords):
    """ Looks at the list of codewords for a block cipher and determines block length. Checks whether codeword length
     is consistent.

    :param codewords: The list of codewords used for a block-code encoding.
    :return: The apparent block length.
    """

    block_size = len(codewords[0])

    for w in codewords:
        if len(w) != block_size:
            # Block code only makes sense if all blocks are the same length - tehrefore the codewords should be of equal length as well.
            raise Exception('Inconsistent block size in codebook.')

    return block_size
