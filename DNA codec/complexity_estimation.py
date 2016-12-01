"""Methods used to estimate complexity (repetitiveness) of a DNA sequence.

Author: Azat Akhmetov <azat@utexas.edu>
"""
import math


def __list_unique_kmers(s, k):
    """ Lists unique k-mers present in s.
    """
    kmers = set()
    for i in range(len(s)-k+1):
        w = s[i:i+k]
        kmers.add(w)
    return list(kmers)


def __number_of_all_unique_kmers(s):
    """ Finds the number of unique k-mers in s for all k in [1, len(s)].
    """
    n = len(s)
    uniques = set()
    for k in range(1, n+1):
        uniques.update(__list_unique_kmers(s, k))

    return len(uniques)


def __number_of_possible_kmers(n):
    """ Finds the number of possible k-mers for each k in [1, n] that can be contained in a string of length n.
    """
    kmer_counts = []
    for i in range(n):
        k = i+1
        num = min(int(math.pow(4, k)), n-i)
        kmer_counts.append(num)

    return sum(kmer_counts)


def estimate_complexity_by_counting_kmers(w):
    """ Tries to estimate Kolmogorov complexity of w, by comparing the number of observed unique k-mers to the number
    of possible unique k-mers in a string of this length.
    """
    n = len(w)
    observed = __number_of_all_unique_kmers(w) - n
    expected = __number_of_possible_kmers(n) - n

    return observed / expected


def __test_with_codewords():
    all_words = open('Intermediate data/Starting wordlists/codewords.txt', 'r').read().splitlines()

    rates = {}
    for w in all_words:
        rates[w] = estimate_complexity_by_counting_kmers(w)


    for key in sorted(rates, key=rates.get):
        print("{0} - {1}".format(key, rates[key]))