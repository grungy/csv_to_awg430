import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
sns.set_theme()

str_header = b"MAGIC 1000\r\n#"
tek_dtype = np.dtype([('vals', 'f4'), ('marker', 'u1')])

def read_lecroy_csv(fn):
    with open(fn, 'r', encoding='ISO-8859-1') as f:
        first_line = f.readline().strip().split(",")
        assert( first_line == "LECROYHDO6104A-MOÅ,50511,Waveform".split(",")), repr(first_line)
        _, num_segments, _, sz_segment = f.readline().strip().split(",")
        _ = f.readline()
        ix_segment, time_trig, time_since_segment = f.readline().strip().split(",")
        tmp_locals = locals()
        dct_meta = dict(filter(lambda elem: elem[0] not in ["fn", "f", "first_line", "_"], tmp_locals.items()))
        data = np.loadtxt(fn, skiprows=5, delimiter=',', encoding='ISO-8859-1')
        t_step = data[0, 0] - data[1, 0]
        t_start = data[0, 0]
    return data[:, 1], t_start, t_step

def lecroy_to_numpy(fn_in, fn_out):
    data, t_start, t_step = read_lecroy_csv(fn_in)
    data_out = np.zeros(len(data), dtype=tek_dtype)
    data_out['vals'] = data
    return data_out, t_start, t_step

def lecroy_to_awg430(fn_in, fn_out):
    data, t_start, t_step = read_lecroy_csv(fn_in)
    data_out = np.zeros(len(data), dtype=tek_dtype)
    data_out['vals'] = data
    write_wfm(data_out, fn_out, clock=1./t_step)
    return data_out, t_start, t_step

def write_wfm(data, fn_out, clock=None):
    """""" 
    str_n_bytes = b"%d" % data.nbytes
    header = str_header + (b"%d" % len(str_n_bytes)) + str_n_bytes
    trailer = b"" if not clock else (b"CLOCK %g\r\n" % clock)

    str_out = header + data.tobytes() + trailer
    with open(fn_out, 'wb') as f:
        f.write(str_out)
    
    return

if __name__ == "__main__":

    filename1 = ''
    filename2 = ''

    data1, t_start1, t_step1 = lecroy_to_numpy(filename1)

    data2, t_start2, t_step2 = lecroy_to_numpy(filename2)

    assert t_step1 != t_step2, print("time steps don't match")

    data_out = data1 - data2

    fn_out = 'data_diff'
    write_wfm(data_out, fn_out, clock=1./t_step1)
    print("complete")
    


