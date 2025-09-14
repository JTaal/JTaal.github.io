import numpy as np
import mpmath as mp
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

def riemann_sound_to_wav(t_min=0, t_max=50, samples=44100, filename="riemann.wav"):
    """
    Generate .wav file of ζ(0.5 + i t) along the critical line.
    Combines Re and Im parts, finds zeros, and computes wavelength/frequency.
    """
    # Sampling points
    t_vals = np.linspace(t_min, t_max, samples)
    z_vals = [mp.zeta(0.5 + 1j*t) for t in t_vals]
    
    # Combine into signal (normalize to [-32767, 32767] for WAV)
    signal = np.array([float(mp.re(z)) + float(mp.im(z)) for z in z_vals])
    signal /= np.max(np.abs(signal))
    signal_int16 = np.int16(signal * 32767)

    # Save as WAV
    write(filename, samples, signal_int16)

    # Find zeros
    re_vals = np.array([float(mp.re(z)) for z in z_vals])
    im_vals = np.array([float(mp.im(z)) for z in z_vals])
    zero_indices = np.where((np.sign(re_vals[:-1]) != np.sign(re_vals[1:])) & 
                            (np.sign(im_vals[:-1]) != np.sign(im_vals[1:])))[0]
    zeros_t = t_vals[zero_indices]

    # Compute wavelengths and frequencies
    diffs = np.diff(zeros_t)
    freqs = 1.0 / diffs

    # Plot
    plt.figure(figsize=(10,4))
    plt.plot(t_vals, signal, label="Re+Im(ζ)")
    plt.scatter(zeros_t, np.zeros_like(zeros_t), color="red", zorder=3, label="Zeros")
    plt.legend()
    plt.xlabel("t (imag part of s = 0.5+it)")
    plt.ylabel("Signal amplitude")
    plt.title("Sound signal from ζ(0.5+it)")
    plt.show()

    return zeros_t, diffs, freqs
zeros, wavelengths, frequencies = riemann_sound_to_wav(0, 50)

print("First few zeros:", zeros)
print("Wavelengths:", wavelengths)
print("Frequencies:", frequencies)
