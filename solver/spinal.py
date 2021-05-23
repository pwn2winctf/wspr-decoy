# Copyright (c) 2021 Paulo Matias
# Based on the reference Spinal decoder
# Copyright (c) 2012 Jonathan Perry
# License: MIT

from hashlib import sha3_224
from functools import reduce


def encode(seed, M, size, k=4):
    # generate spine values
    s_i = b''
    spine = []
    for i in range(0, len(M), k):
        m_i = bytes([int('0b' + M[i:i+k], 2)])
        s_i = h(s_i, m_i)
        spine.append(s_i)
    symbols = []
    # generate symbols
    rng_bits = size // len(spine)
    for i, s_i in enumerate(spine):
        b = rng_bits
        if i == len(spine) - 1:
            # use additional bits for the last spine value
            b += size % len(spine)
        symbols.append(rng(s_i, seed, b))
    # interleave symbols
    res = []
    for i in range(rng_bits):
        for symbol in symbols:
            res.append(symbol[i])
    res.extend(symbols[-1][rng_bits:])
    return [float(symbol) for symbol in res]


def decode(seeds, frames, M_len, k=4, B=256, d=1):
    frame_size = len(frames[0])
    spine_len = (M_len + k - 1) // k
    rng_bits = frame_size // spine_len

    # deinterleave symbols
    symbols = [[[] for _ in range(len(frames))] for _ in range(spine_len)]
    for i, frame in enumerate(frames):
        j = 0
        for _ in range(rng_bits):
            for l in range(spine_len):
                symbols[l][i].append(frame[j])
                j += 1
        symbols[-1][i].extend(frame[j:])

    wavefront = [(0, b'', [])]

    # expand then prune wavefront, one spine value at a time
    for cur_spine_symbols in symbols:
        new_wavefront = []

        # For each node in the current wavefront
        for (path_metric, spine_value, path) in wavefront:
            # For each possible message block (2^k options)
            for edge in range(1 << k):
                # Calculate the new spine value
                new_spine_value = h(spine_value, bytes([edge]))

                edge_metric = 0

                for seed, cur_seed_symbols in zip(seeds, cur_spine_symbols):
                    # What the transmitter would have produced if it had this spine value
                    rng_values = map(float,
                                     rng(new_spine_value, seed, len(cur_seed_symbols)))

                    # Go over all received symbols, and compute the edge metric
                    for node_symbol, received_symbol in zip(rng_values, cur_seed_symbols):
                        # Add the distance squared to the edge metric
                        distance = received_symbol - node_symbol
                        edge_metric += distance * distance

                # The new path metric is the sum of all edges from the root
                new_path_metric = path_metric + edge_metric

                # Add new node to wavefront
                new_wavefront.append(
                    (new_path_metric, new_spine_value, path + [edge]))

        wavefront = prune(new_wavefront, k, B, d)

    # get the node with the smallest path metric. Note that this code breaks
    #   ties in favor of nodes with smaller spine value.
    _, _, path = min(wavefront)

    res = []
    for block in path:
        res.append(bin(block)[2:].rjust(k, '0'))
    return ''.join(res)


def prune(wavefront, k, B, d):
    """
    Given a wavefront with several sub-trees, prune to only keep the best B
        sub-trees
    """

    # We prune in the granularity of sub-trees, each one has d layers.
    # The leaves of these sub-trees are in the wavefront.
    # Each subtree has 2^(k(d-1)) such leaves in the wavefront.
    num_subtree_nodes = (1 << (k * (d - 1)))

    # Split nodes according to subtree.
    # subtrees is a list, each of its components is a list 2^(k(d-1)) nodes
    subtrees = []
    while len(wavefront) > 0:
        # add the first 2^(k(d-1)) nodes to 'subtrees'
        subtrees.append(wavefront[:num_subtree_nodes])
        # remove the first 2^(k(d-1)) nodes from 'wavefront'
        wavefront = wavefront[num_subtree_nodes:]

    # sort subtrees according to the minimum path metric of nodes in the
    # subtree
    subtrees.sort(key=lambda x: min(y[0] for y in x))

    # take only <= B sub-trees with best scores
    subtrees = subtrees[:B]

    # Set wavefront with all nodes in the retained sub-trees
    return reduce(lambda x, y: x+y, subtrees)


def h(s_i, m_i):
    return sha3_224(s_i + m_i).digest()


def rng(s_i, seed, nbits):
    assert nbits <= 8
    # our variant of the algorithm uses an additional seed so that different
    # frames containing the same data result in different symbols
    bits = bin(sha3_224(s_i + seed).digest()[-1])[2:].rjust(8, '0')
    return bits[8-nbits:]
