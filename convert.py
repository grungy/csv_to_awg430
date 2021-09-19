import numpy as np
import struct

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

def pack_data_str(data, num_bytes):
    waveform = "{0:0{1}x}".format(int(data),num_bytes)
    marker = (0).to_bytes(1, byteorder='little')
    return waveform + str(marker)

if __name__ == "__main__":
    
    num_bytes = 10
    num_digits = 2
    num_bytes_uni = num_to_unicode(num_bytes)
    num_digits_uni = num_to_unicode(num_digits)
    
    marker = (0).to_bytes(1, byteorder='little')
    print(marker)

    data = 48
    data_str = pack_data_str(data, num_bytes)
    print("data_str:\n", data_str)

    clock = 1 * 10e8
    HEADER = "MAGIC 1000\r\n"
    BODY = "{}{}{}{}".format(hex(ord('#'))[2:], num_digits_uni, num_bytes_uni, data_str)
    print("\nBODY:\n", BODY)

    TRAILER = "CLOCK {}\r\n".format(clock)
    MSG = "{}{}{}".format(hex(string_to_int(HEADER))[2:], BODY, hex(string_to_int(TRAILER))[2:])
    print("\nMSG\n", MSG)

    PDU = string_to_int(MSG)
    print("\nPDU\n", hex(PDU))

    # s = '0123456789'
    # x = string_to_int(s)
    # print(hex(x))