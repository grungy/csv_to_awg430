from random import sample
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def resample_data(T, X, new_sample_rate):
    # desired sample rate / input sample rate * number of points in input signal
    dt = 1 / new_sample_rate
    dt_old = (T.max() - T.min()) / T.size
    old_sample_rate = 1 / dt_old
    num_points_new = int((old_sample_rate / new_sample_rate) * T.size)
    
    Told = np.linspace(T.min(), T.max(), T.size)
    F = interp1d(Told, X, fill_value='extrapolate')
    Tnew = np.linspace(T.min(), T.max(), num_points_new)
    Xnew = F(Tnew)
    print(Told.min(), Told.max(), Told.size)
    print(Tnew.min(), Tnew.max(), Tnew.size)
    print(Told)
    print(Tnew)
    return Tnew, Xnew

if __name__ == "__main__":

    T = np.random.exponential(size=10).cumsum()
    T = np.linspace(0, 100, 1000)
    X = np.random.normal(size=1000)
    X = np.square(T)

    sample_rate = int(100)  # samples / time (seconds)
    
    Tnew, Xnew = resample_data(T, X, sample_rate)
    
    # Plot the output of the subtraction. 
    plt.plot(T, X, '.', label="Original Data (1000 Samples Per Second)")
    plt.plot(Tnew, Xnew, 'x', label="Downsampled Data (100 Samples Per Second)")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (V)")
    plt.title("Interpolation Test")
    plt.legend()
    plt.show()