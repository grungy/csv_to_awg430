import numpy as np
import struct
import itertools

def string_to_int(s):
    nchars = len(s)
    # string to int or long. Type depends on nchars
    x = sum(ord(s[byte])<<8*(nchars-byte-1) for byte in range(nchars))
    return x

def num_to_unicode(num):
    num_lst = [a for a in str(num)]
    uni = [ord(a) for a in num_lst]
    uni_hx = [hex(a)[2:] for a in uni]
    output = ''.join(uni_hx)
    return output

def pack_data_unit(n, m=0):
    return struct.pack('<fb', n, m)

def pack_data(nums, num_bytes=0, num_digits=0):
    """nums is a list of floats"""
    endianness = '<'
    unit = 'fb'
    mod_str = ''.join([endianness, unit * len(nums)])
    print(mod_str)
    lst = list(zip(nums, [0] * (len(nums))))
    lst = list(itertools.chain(*lst))
    print(lst)
    packed = struct.pack(mod_str, *lst)
    print(struct.unpack(mod_str, packed))
    return packed


def pack_data_str(data, num_bytes, num_digits):
    data_bytes = struct.pack('f', data)
    marker = str(0)
    waveform = "{0:0{1}x}".format(int(data), num_bytes - num_digits)
    data_pdu = waveform + marker
    print("waveform: ", waveform)
    return data_pdu

if __name__ == "__main__":
    
    nums = range(0, 5)
    print(nums)
    x = pack_data(nums)
    print(x)

    # num_bytes = 10
    # num_digits = 2
    # num_bytes_uni = num_to_unicode(num_bytes)
    # num_digits_uni = num_to_unicode(num_digits)

    # data = 3
    # data_str = pack_data_str(data, num_bytes, num_digits)
    # print("data_str:\n", data_str)

    # clock = 1 * 10e8
    # HEADER = "MAGIC 1000\r\n"
    # BODY = "{}{}{}{}".format(hex(ord('#'))[2:], num_digits_uni, num_bytes_uni, data_str)
    # print("\nBODY:\n", BODY)

    # TRAILER = "CLOCK {}\r\n".format(clock)
    # MSG = "{}{}{}".format(hex(string_to_int(HEADER))[2:], BODY, hex(string_to_int(TRAILER))[2:])
    # print("\nMSG\n", MSG)

    # PDU = string_to_int(MSG)
    # print("\nPDU\n", hex(PDU))

    # s = '0123456789'
    # x = string_to_int(s)
    # print(hex(x))