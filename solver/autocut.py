#!/usr/bin/env python
# This tool cuts a wav file so that it starts when the WSPR transmission starts.
# Please cut all wav files before using them as input to the solver.
import subprocess
import tempfile
import shutil
import wave
import sys
import os
import re


def samples_at(infile, offset):
    inwav = wave.open(infile, 'rb')
    samples = inwav.readframes(inwav.getnframes())
    samples = samples[int(inwav.getsampwidth()*offset*inwav.getframerate()):]
    return inwav, samples


def cut(infile, offset):
    inwav, samples = samples_at(infile, offset)
    outfile = tempfile.NamedTemporaryFile(mode='wb', suffix='.wav')
    outwav = wave.open(outfile, 'wb')
    outwav.setparams(inwav.getparams())
    outwav.writeframes(samples)
    return outfile


def num_seconds(infile):
    inwav = wave.open(infile, 'rb')
    return inwav.getnframes()/inwav.getframerate()


def wsprd(filename, search_for='PU2UID'):
    p = subprocess.Popen(['./wsprd',
                          '-a', os.path.join(os.getenv('HOME')
                                             or '.', '.wspr'),
                          filename],
                         stdout=subprocess.PIPE,
                         encoding='utf-8')
    for line in p.stdout:
        if line.strip() == '<DecodeFinished>':
            return None
        arr = re.split(r'\s+', line.strip())
        if len(arr) == 8:
            _, _, dt, freq, _, callsign, _, _ = arr
            if callsign == search_for:
                return (float(dt), 1e6*float(freq))


def search_start(infile):
    for offset in range(0, int(num_seconds(infile) - 110), 5):
        tmp = cut(infile, offset)
        res = wsprd(tmp.name)
        tmp.close()
        if res:
            dt, freq = res
            return offset + dt, freq


def main(filename):
    res = search_start(filename)
    if res is None:
        print('{}: could not find callsign!'.format(filename), file=sys.stderr)
        return
    offset, freq = res
    print('{}: offset={}, freq={}'.format(filename, offset, freq))
    tmp = cut(filename, offset)
    shutil.copy(tmp.name, filename)


if __name__ == '__main__':
    main(sys.argv[1])
