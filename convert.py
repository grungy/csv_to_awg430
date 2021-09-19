import numpy as np

def string_to_int(s):
    nchars = len(s)
    # string to int or long. Type depends on nchars
    x = sum(ord(s[byte])<<8*(nchars-byte-1) for byte in range(nchars))
    return x

def pack_data_str(data, num_bytes):
    data_bytes = "{0:0{1}x}".format(int(data),num_bytes)
    return data_bytes

if __name__ == "__main__":
    
    num_bytes = 10
    num_digits = 2
    data = 0x0000000000003000
    data = 48
    data_str = pack_data_str(data, num_bytes)
    print("data_str:\n", data_str)

    clock = 1 * 10e8
    HEADER = "MAGIC 1000\r\n"
    BODY = "#{}{}{}".format(num_digits, num_bytes, data_str)
    print("\nBODY:\n", BODY)

    TRAILER = "CLOCK {}\r\n".format(clock)
    MSG = "{}{}{}".format(HEADER, BODY, TRAILER)
    print("\nMSG\n", MSG)

    PDU = string_to_int(MSG)
    print("\nPDU\n", hex(PDU))

    # s = '0123456789'
    # x = string_to_int(s)
    # print(hex(x))