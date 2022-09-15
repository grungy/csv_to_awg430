from random import sample
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy import signal

def resample_data(T, X, new_sample_rate):
    # desired sample rate / input sample rate * number of points in input signal
    dt = 1 / new_sample_rate
    F = interp1d(T, X, fill_value='extrapolate')
    Tnew = np.arange(T.min(), T.max(), dt)
    Xnew = F(Tnew)
    return Tnew, Xnew

def scipy_resample_data(T, X, new_sample_rate):
    pass

if __name__ == "__main__":

    T = np.random.exponential(size=10).cumsum()
    sample_rate = 1e3
    dt = 1 / sample_rate
    T = np.arange(0, 100, dt)
    X = np.random.normal(size=T.size)
   
    x = np.linspace(0, 10, 20, endpoint=False)
    y = np.cos(-x**2/6.0)
    f = signal.resample(y, 100)
    f_poly = signal.resample_poly(y, 100, 20)
    xnew = np.linspace(0, 10, 100, endpoint=False)

    sample_rate = int(100)  # samples / time (seconds)
    
    Tnew, Xnew = resample_data(x, y, sample_rate)
    
    # Plot the output of the subtraction. 
    plt.plot(x, y, '-', label="Original Data (1000 Samples Per Second)")
    plt.plot(xnew, f, 'x', label="Downsampled Data (100 Samples Per Second)")
    plt.plot(Tnew, Xnew, 'x', label="Downsampled Data (100 Samples Per Second)")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (V)")
    plt.title("Interpolation Test")
    plt.legend()
    plt.show()