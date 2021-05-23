#!/usr/bin/env python
from hashlib import sha3_224
from random import gauss, randint
from spinal import encode, decode
from math import sqrt
import os

num_frames = 6*12

signal_power = 0.25
noise_power = signal_power
noise_std_dev = sqrt(noise_power)
impulsive_noise_power = 128*signal_power
impulsive_noise_std_dev = sqrt(noise_power)
impulsive_noise_len = 20

M_len = 5*32
M = ''.join(str(os.urandom(1)[0] & 1) for _ in range(M_len))

print('orig msg', M)

seeds = []
frames = []

for _ in range(num_frames):
    seed = sha3_224(os.urandom(224//8)).digest()
    symbols = encode(seed, M, 162)
    start = randint(0, 162-impulsive_noise_len)
    symbols = [sym + gauss(0,
        impulsive_noise_std_dev if (i>=start and i<=start+impulsive_noise_len)
        else noise_std_dev) for i, sym in enumerate(symbols)]
    seeds.append(seed)
    frames.append(symbols)

dec_M = decode(seeds, frames, M_len)
print('decoded msg', dec_M)

err_bits = sum(a != b for a, b in zip(M, dec_M))
print('errored bits', err_bits)
print('err ratio', err_bits / M_len)
