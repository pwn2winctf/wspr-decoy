#!/usr/bin/env python3
from spinal import decode
from hashlib import sha3_224
from datetime import datetime
from dateutil.parser import parse
import scipy.signal.windows as windows
import numpy as np
import os
import re
import sys
import subprocess


def random_freq(seed):
    r = sha3_224(seed).digest()[0]/255
    return int(7040000 + (200-6-23)*r)


def recording_time(filename):
    filename = os.path.basename(filename)
    m = re.search(r'(\d{4}-\d{2}-\d{2})T(\d{2})_(\d{2})_(\d{2}Z)', filename)
    if m:
        return parse('{} {}:{}:{}'.format(*m.groups())).timestamp()
    m = re.search(r'-(\d+).wav', filename)
    if m:
        return int(m.group(1))
    raise ValueError(
        'time spec in filename {} not recognized'.format(filename))


def wsprd(filename):
    p = subprocess.Popen(['./wsprd',
                          '-a', os.path.join(os.getenv('HOME')
                                             or '.', '.wspr'),
                          filename],
                         stdout=subprocess.PIPE,
                         encoding='utf-8')
    for line in p.stdout:
        if line.strip() == '<DecodeFinished>':
            return None
        if line.startswith('AM=>'):
            return np.array([float(x) for x in line.strip().split(' ', 2)[1].split(',') if x != ''])


def equalize(a, hwsz=4, std=3):
    weights = windows.gaussian(2*hwsz, std=std)
    b = np.zeros(len(a))
    for i in range(len(a)):
        if i < hwsz:
            win = a[0:2*hwsz]
        elif i+hwsz >= len(a):
            win = a[-2*hwsz:]
        else:
            win = a[i-hwsz:i+hwsz]
        mean = np.average(win, weights=weights)
        std = np.sqrt(np.average((win-mean)**2, weights=weights))
        b[i] = .5 + .5*(a[i] - mean)/std
    return b


def bits_to_string(bits):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ{}-_?!'
    bits_per_char = 5
    assert 1 << bits_per_char == len(alphabet)
    assert len(bits) % bits_per_char == 0
    s = ''
    for i in range(0, len(bits), bits_per_char):
        s += alphabet[int('0b' + bits[i:i+bits_per_char], 2)]
    return s


def main(filenames):
    at_min = 0

    assert at_min % 2 == 0

    seeds = []
    frames = []

    for filename in filenames:
        print('=> {}'.format(filename))

        timestamp = recording_time(filename)
        next_timestamp = 60*at_min + 600*((timestamp + 600) // 600)

        seed = sha3_224(b'%d' % next_timestamp).digest()

        freq = random_freq(seed)

        print('PRNG seed = {}'.format(seed.hex()))
        print('Waiting until {} to TX at {} Hz'.format(
            datetime.fromtimestamp(next_timestamp).strftime(
                '%Y-%m-%d %H:%M:%S'),
            freq))

        am_received = wsprd(filename)
        print('AM received:', am_received)

        am_symbols = equalize(am_received)
        print('AM equalized:', am_symbols)

        seeds.append(seed)
        frames.append(am_symbols)

    print('=> running spinal decoder')
    M_len = 5*32
    dec_M = decode(seeds, frames, M_len)
    print('decoded bits:', dec_M)

    print('decoded string:', bits_to_string(dec_M))


if __name__ == '__main__':
    main(sys.argv[1:])
