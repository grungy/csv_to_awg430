import struct
# from bitstring import BitArray, BitStream
import bitstring
import numpy as np

class FormatError(Exception):
  pass

def num_to_ascii(num):
    """returns a string of the decimal ascii representation for use with bitstring"""
    arr = bytes(str(num), 'ascii').hex()
    return str(int(arr, 16))

def str_to_ascii(s):
    arr = bytes(s, 'ascii').hex()
    return '0x' + arr

def encode_header():
    """returns a dict of wfm metadata"""
    
    fmt = 'header, uint:8=num_digits, uint:16=num_bytes'

    d = {'header': '0x4D4147494320313030300D0A23',
        'num_digits': num_to_ascii(2),
        'num_bytes': num_to_ascii(10)
        }

    s = bitstring.pack(fmt, **d)
    return s

def encode_data(array):
    """Takes a numpy array of data in and converts it into a bitstring"""
    z = np.zeros(array.shape)
    zipped = np.c_[array, z]
    d = dict(enumerate(zipped.flatten(), 0))
    d2 = {}
    # print(d)

    fmt = ""
    toggle = True

    for k,v in d.items():
        d2[str(k)] = v
        if toggle:
            fmt = fmt + 'float:32={}, '.format(k)
            toggle = False
        else:
            fmt = fmt + 'uint:8={}, '.format(k)
            toggle = True
    d2['2'] = 30
    fmt = fmt[:-2]
    print(fmt)
    print(d2)

    s = bitstring.pack(fmt, **d2)
    return s

def encode_trailer():
    trailer_str = "CLOCK {}\r\n".format(float(1 * 10e8))
    fmt = 'trailer'
    d = {
        'trailer': str_to_ascii(trailer_str)
    }
    s = bitstring.pack(fmt, **d)
    return s


if __name__ == "__main__":
    header = encode_header()
    arr = np.arange(0, 2)
    arr = np.zeros(arr.shape)
    data = encode_data(arr)
    trailer = encode_trailer()
    print(trailer)
    
    total = bitstring.BitArray()
    total.append(header)
    total.append(data)
    total.append(trailer)
    
    f = open('test.hex', 'wb')
    total.tofile(f)