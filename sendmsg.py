#!/usr/bin/env python3
from modulator import modulator
import sys
import re
import string


class WSPR:
    """ https://github.com/brainwagon/genwspr """
    syncv = [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0,
    1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1,
    0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0,
    0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0,
    0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0]

    @staticmethod
    def normalizecallsign(callsign):
        callsign = list(callsign)
        idx = None
        for i, ch in enumerate(callsign):
            if ch in string.digits:
                idx = i
        assert idx is not None
        newcallsign = 6 * [" "]
        newcallsign[2-idx:2-idx+len(callsign)] = callsign
        return ''.join(newcallsign)

    @staticmethod
    def encodecallsign(callsign):
        callsign = WSPR.normalizecallsign(callsign)
        lds = string.digits + string.ascii_uppercase + " "
        ld = string.digits + string.ascii_uppercase
        d = string.digits
        ls = string.ascii_uppercase + " "
        acc = lds.find(callsign[0])
        acc *= len(ld)
        acc += ld.find(callsign[1])
        acc *= len(d)
        acc += d.find(callsign[2])
        acc *= len(ls)
        acc += ls.find(callsign[3])
        acc *= len(ls)
        acc += ls.find(callsign[4])
        acc *= len(ls)
        acc += ls.find(callsign[5])
        return WSPR.tobin(acc, 28)

    @staticmethod
    def tobin(v, l):
        x = []
        while v != 0:
            x.append(str(v % 2))
            v = v // 2 
        while len(x) < l:
            x.append("0")
        x.reverse()
        return ''.join(x)[0:l]

    @staticmethod
    def grid2ll(grid):
        if re.match(r'[A-R][A-R][0-9][0-9]([a-x][a-x])?$', grid):
            # go ahead and decode it.
            p = (ord(grid[0])-ord('A'))
            p *= 10
            p += (ord(grid[2])-ord('0'))
            p *= 24
            if len(grid) == 4:
                p += 12
            else: 
                p += (ord(grid[4])-ord('a')) + 0.5
            lng = (p / 12) - 180.0
            p = (ord(grid[1])-ord('A'))
            p *= 10
            p += (ord(grid[3])-ord('0'))
            p *= 24
            if len(grid) == 4:
                p += 12
            else: 
                p += (ord(grid[5])-ord('a')) + 0.5
            lat = (p / 24) - 90.0
            return (lat, lng)
        else:
            raise ValueError('Malformed grid reference "%s"' % grid)

    @staticmethod
    def encodegrid(grid):
        lat, long = WSPR.grid2ll(grid)
        long = int((180 - long) / 2.0)
        lat = int(lat + 90.)
        return WSPR.tobin(long * 180 + lat, 15)

    @staticmethod
    def encodepower(power):
        power = int(power)
        power = power + 64
        return WSPR.tobin(power, 7)

    class convolver:
        def __init__(self):
            self.acc = 0
        def encode(self, bit):
            self.acc = ((self.acc << 1) & 0xFFFFFFFF) | bit
            return WSPR.parity(self.acc & 0xf2d05351), WSPR.parity(self.acc & 0xe4613c47)

    @staticmethod
    def encode(l):
        e = WSPR.convolver()
        f = []
        l = map(lambda x : int(x), list(l))
        for x in l:
            b0, b1 = e.encode(x)
            f.append(b0)
            f.append(b1)
        return f

    @staticmethod
    def parity(x):
        even = 0
        while x:
            even = 1 - even
            x = x & (x - 1)
        return even

    @staticmethod
    def bitstring(x):
        return ''.join([str((x>>i)&1) for i in (7, 6, 5, 4, 3, 2, 1, 0)])

    @staticmethod
    def bitreverse(x):
        bs = WSPR.bitstring(x)
        return int(bs[::-1], 2)

    @staticmethod
    def produce_symbols(callsign, grid, power):
        idx = range(0, 256)
        ridx = list(filter(lambda x : x < 162, map(lambda x : WSPR.bitreverse(x), idx)))

        callsign = WSPR.encodecallsign(callsign)
        grid = WSPR.encodegrid(grid)
        power = WSPR.encodepower(power)

        message = callsign + grid + power + 31 * '0'
        message = WSPR.encode(message)

        # interleave...
        imessage = 162 * [0]

        for x in range(162):
            imessage[ridx[x]] = message[x]

        return [(2*x+y) for x, y in zip(imessage, WSPR.syncv)]


print(WSPR.produce_symbols('PU2UID', 'GG68', 40))
