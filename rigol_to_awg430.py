import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
sns.set_theme()

str_header = b"MAGIC 1000\r\n#"
tek_dtype = np.dtype([('vals', 'f4'), ('marker', 'u1')])

class WfmReadError(Exception):
    """error for unexpected things"""
    pass

def read_csv(fn):
    with open(fn, 'r') as f:
        first_line = f.readline().strip().split(",")
        assert( first_line == "CH1,Start,Increment,".split(",")), repr(first_line)
        unit, str_t_start, str_t_step = f.readline().split(",")
        data = np.loadtxt(fn, skiprows=2, delimiter=',', usecols=0)
    return data, float(str_t_start), float(str_t_step)

def read_wfm(target):
    """return sample data from target WFM file"""
    
    with open(target, 'rb') as f:
        hbytes = f.read(len(str_header))
        assert (hbytes == str_header), "Failed to find MAGIC. FOUND: " + repr(hbytes)
        num_digits = int(f.read(1))
        num_bytes = int(f.read(num_digits))

        
        data = np.frombuffer(f.read(num_bytes), dtype=tek_dtype)
        
        print(data.nbytes)
        trailer = f.read()
        return str_header, data, trailer

def write_wfm(data, fn_out, clock=None):
    """""" 
    str_n_bytes = b"%d" % data.nbytes
    header = str_header + (b"%d" % len(str_n_bytes)) + str_n_bytes
    trailer = b"" if not clock else (b"CLOCK %g\r\n" % clock)

    str_out = header + data.tobytes() + trailer
    with open(fn_out, 'wb') as f:
        f.write(str_out)
    
    return

def rigol_to_awg430(fn_in, fn_out):
    data, t_start, t_step = read_csv(fn_in)
    data_out = np.zeros(len(data), dtype=tek_dtype)
    data_out['vals'] = data
    write_wfm(data_out, fn_out, clock=1./t_step)
    return data_out, t_start, t_step
        
def decode_header(header_bytes):
    """returns a dict of wfm metadata"""
    str_header = "MAGIC 1000\r\n#"
    return str_header

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Rigol Oscilloscope trace file to AWG430 waveform file.')
    parser.add_argument('filename', help='Input CSV file to be read.')
    parser.add_argument('--plot', '-p',
    action='store_true',
    help='Plot the data read from the csv after writing the wfm file.' )
    parser.add_argument('--output', '-o', help='Output filename to use.')   

    args = parser.parse_args()

    if(args.output):
        data, t_start, t_step = rigol_to_awg430(args.filename, args.output+".wfm")
    else:
        basename = os.path.basename(args.filename).split(".")[0]
        data, t_start, t_step = rigol_to_awg430(args.filename, basename+".wfm")

    if(args.plot):
        print("Start, {} Step: {}".format(t_start, t_step))
        print("Data Shape: {}".format(data.shape))

        plt.plot(data['vals'])
        plt.show()
