# Copyright (c) 2012 Jonathan Perry
# This code is released under the MIT license (see LICENSE file).
'''
This is an example of the python implementation of spinal codes. A simple 
    "hello world" message is encoded, white gaussian noise with some SNR is 
    added, and the noisy data is then fed into the decoder.

This example produces constellation points with 8-bit precision. The noisy 
    symbols are quantized to integers, and all path metrics are done with
    integer arithmetic.
'''

# some constants:

k = 4
c = 1
precision = 8
B = 256
d = 1
passes = k*3

# Message to be encoded:
message = b"hello world!"

# expected encoder output
expected_encoder_output = [184, 108, 36, 108, 253, 68, 204, 119, 243, 141, 170, 56, 101, 97, 252, 79, 95, 236, 207, 191, 158, 89, 82, 151, 141, 255, 100, 112, 233, 220, 20, 146, 16, 108, 24, 117, 178, 175, 39, 210, 134, 224, 220, 75, 231, 4, 182, 189, 29, 59, 129, 105, 60, 64, 207, 253, 161, 41, 146, 10, 249, 210, 175, 121, 121, 37, 46, 239, 208, 18, 42, 101, 61, 67, 136, 166, 62, 192, 44, 43, 240, 97, 196, 228, 91, 94, 242, 9, 130, 218, 243, 208, 16, 248, 57, 194]

if __name__ == '__main__':
    from Encoder import Encoder
    from Decoder import Decoder
    from SymbolMapper import SymbolMapper
    import random
    import math
    
    mapper = SymbolMapper(c, precision)
    map_func = lambda value: mapper.map(value)
    
    #Instantiate an encoder
    print('Message string: %r' % message)
    print('Message hex:', message.hex())
    encoder = Encoder(k, map_func, message)
    
    # spine length
    n = 8 * len(message)
    spine_length = (n + (k - 1)) // k
    
    print("Producing {} passes.".format(passes))
    symbols = [encoder.get_symbol(i) for i in list(range(spine_length))*passes]
    # additional passes for last spine value
    #symbols.extend(encoder.get_symbol(spine_length-1) for _ in range(passes))
    print("symbols: ", symbols)
    
    # make sure we got the expected result
    #assert(expected_encoder_output == symbols)
    
    # get average signal power
    signal_power = mapper.get_signal_average_power()
    
    # what is the noise power and standard deviation when SNR is 10dB?
    noise_power = signal_power
    noise_std_dev = math.sqrt(noise_power)
    
    # initialize random number generator. this seed is fixed constant in order
    # to get deterministic results in this example.
    #random.seed(3918491349)
    
    # add white gaussian noise at 10dB to signal
    print("Adding white gaussian noise at 10dB.")
    noisy_symbols = [sym + random.gauss(0, noise_std_dev) for sym in symbols]
    # round to closest integer
    noisy_symbols = [int(x + 0.5) for x in noisy_symbols]
    print("noisy symbols:", noisy_symbols)
    
    # instantiate decoder
    decoder = Decoder(k, B, d, map_func)
    
    # update decoder with gathered points
    for i in range(spine_length):
        points=[noisy_symbols[i+j*spine_length] for j in range(passes)]
        #if i == spine_length - 1:
        #    points.extend(noisy_symbols[:-passes])
        decoder.advance(points)
    
    res = decoder.get_most_likely()
    print("decoded: ", res)
    print("decoded hex:", res.hex())
    
    # make sure we got the message we started with
    #assert(decoder.get_most_likely() == message)
