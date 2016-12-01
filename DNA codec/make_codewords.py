"""Methods for constructing a set of codewords, according to defined constraints such as desired GC ratios, distinctness
(as measured by Levenshtein distance) and repetitiveness. The codewords are intended for use with a block cipher based
scheme for encoding digital information as DNA.

Note that this algorithm isn't fully deterministic. If run repeatedly with the same parameters, the results will often
vary trivially, and sometimes may vary non-trivially. Usually a handful of runs are sufficient to generate a satisfactory
codeword list, which can then be reused for all subsequent work.

Author: Azat Akhmetov <azat@utexas.edu>
"""
import itertools
import networkx
import complexity_estimation

# Inputs and parameters
codeword_length = 4  # number of symbols in each codeword
max_distance = 1  # Levenshtein distance representing the maximum number of mutations (including indels) that may be tolerated in each codeword while allowing recovery of the original word

path_to_generated_codeword_list = 'Output/codewords.txt'  # Where to put the resulting list of codewords

path_to_initial_codewords = 'Intermediate data/Codeword generation/codewords.txt'
path_to_initial_indels = 'Intermediate data/Codeword generation/indels.txt'
path_to_initial_nodelist = 'Intermediate data/Codeword generation/Starting nodes list.txt'


def main():
    """Uses a graph-pruning algorithm to generate a set of codewords that can be used to encode information in DNA with
    an error-correcting code.
    """

    def construct_all_words():
        """Constructs a list of all possible codewords and saves them.
        """
        codewords = []
        indels = []
        for i in range(codeword_length - max_distance, codeword_length + max_distance + 1):
            words = [''.join(p) for p in itertools.product(['A', 'C', 'G', 'T'], repeat=i)]

            if i == codeword_length:
                codewords = words
            else:
                indels += words

        open(path_to_initial_codewords, 'w').write("\n".join(codewords))
        open(path_to_initial_indels, 'w').write("\n".join(indels))


    construct_all_words()

    # Load all the initial word lists from files
    candidates = open(path_to_initial_codewords, 'r').read().splitlines()
    indels = open(path_to_initial_indels, 'r').read().splitlines()
    all_words = candidates + indels


    # Construct the graph
    g = networkx.Graph()


    # Add all the nodes to the graph
    for w in all_words:
        g.add_node(w)

        g.node[w]['candidate'] = (len(w) == codeword_length)
        g.node[w]['good'] = (g.node[w]['candidate'] & gc_is_good(w) & not_repetitive(w))
        g.node[w]['codeword'] = False

    # Dump the list of nodes
    nodelist = ['Node\tCandidate\tGood\tCodeword\n']
    for n in g.nodes():
        row = '{0}\t{1}\t{2}\t{3}\n'.format(n, g.node[n]['candidate'], g.node[n]['good'], g.node[n]['codeword'])
        nodelist += row
    open(path_to_initial_nodelist, 'w').writelines(nodelist)

    # Draw edges for adjacent nodes
    import leven
    for w1 in all_words:
        for w2 in all_words:
            if leven.levenshtein(w1, w2) == 1:
                g.add_edge(w1, w2)


    # Assign codewords
    def find_best_candidate(graph, good_seqs):
        # Pick the node from good_nodes which has the most adjacent bad nodes
        # TODO: Maybe instead use fewest adjacent good nodes?
        bad_neighbors = {}
        for n in good_seqs:
            adjacent_bad_sequences = [b for b in graph.neighbors(n) if not graph.node[b]['good']]

            bad_neighbors[n] = len(adjacent_bad_sequences)

        best_seq = min(bad_neighbors, key=bad_neighbors.get)
        return best_seq


    def shortest_path_length(source, target):
        length = networkx.shortest_path_length(g, source, target)

        return length


    good_candidates = [n for n in g.nodes() if g.node[n]['good']]
    while any(good_candidates):
        # Find best codeword candidate (based on how close it is to bad nodes)
        best_candidate = find_best_candidate(g, good_candidates)

        # Color it "codeword"
        g.node[best_candidate]['good'] = False
        g.node[best_candidate]['codeword'] = True
        good_candidates.remove(best_candidate)


        # All nodes which are...
        for n in g.nodes():
            # ...not marked bad to begin with...
            if g.node[n]['good']:
                # ...and are within max_distance*2...
                if shortest_path_length(best_candidate, n) < (max_distance * 2 + 1): # Wrap this in a function distance(node1, node2), then memoize it using python decorators
                    # ...will be colored "bad"...
                    g.node[n]['good'] = False

                    # ...and if they were considered candidates...
                    if n in good_candidates:
                        # ...they won't be anymore
                        good_candidates.remove(n)


    # We're done, print the codewords
    codewords = [n for n in g.nodes() if g.node[n]['codeword']]
    open(path_to_generated_codeword_list, 'w').write('\n'.join(codewords))

    print('Done!')


def gc_is_good(w):
    num_gc = w.count('C') + w.count('G')

    low_gc = num_gc / len(w) < 0.4
    high_gc = num_gc / len(w) > 0.6

    return not (low_gc & high_gc)


def not_repetitive(w):
    complexity = complexity_estimation.estimate_complexity_by_counting_kmers(w)

    return complexity > 0.75


import time
start = time.time()
main()
finish = time.time()
print('Took %.2F secs.' % (finish - start))