
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

# Simulate EEG data
fs = 500  # Sampling frequency
t = np.arange(0, 30, 1/fs)  # 30 seconds of data

# Simulate a good sleeper with stronger low frequency oscillations (theta waves, 4-7 Hz)
good_sleeper_signal = np.sin(2*np.pi*5*t) + np.random.normal(0, 0.5, len(t))

# Simulate an insomniac with stronger high frequency oscillations (beta waves, 12-30 Hz)
insomnia_signal = 0.5 * np.sin(2*np.pi*25*t) + np.random.normal(0, 0.5, len(t))

# Compute the Power Spectral Density for both signals
# f_good, Pxx_good = welch(good_sleeper_signal, fs, nperseg=1024)
# f_insomnia, Pxx_insomnia = welch(insomnia_signal, fs, nperseg=1024)
f_good = np.arange(0.5, 20.25, 0.25)
data = [24.90426595,22.95185214,21.10164441,19.45829797,17.66110363,16.19554884,15.0712171,14.15481915,13.64407193,12.94683309,12.38359764,11.76980703,11.31367773,10.70507284,10.07904781,9.405792263,8.829446458,8.426673844,8.157610248,7.792575248,7.253019375,6.790495757,6.416304598,6.055346392,5.696764925,5.218630255,4.923197326,4.479593678,4.277311376,3.843454789,3.601331028,3.299082585,3.001042204,2.82415158,2.6148483,2.391951195,2.182407565,1.932425405,1.776227227,1.649733688,1.491548111,1.472435526,1.407302189,1.394505394,1.475727067,1.549099012,1.630081023,1.740288782,1.750433726,1.737561213,1.736400352,1.742270498,1.602122088,1.306361195,0.956853745,0.523762535,0.086701775,-0.331199612,-0.681989045,-1.03747979,-1.3587933,-1.563493912,-1.826860021,-2.029084884,-2.209245175,-2.385527564,-2.581963393,-2.704053008,-2.814328287,-2.923367374,-3.022117885,-3.162380336,-3.258947511,-3.419589009,-3.546077463,-3.641033127,-3.688406903,-3.838495082,-3.929968517]
Pxx_good = np.array(data)
# For the statistical significance (t-test p values), we simulate some data
p_values = np.random.uniform(low=0.01, high=0.1, size=len(f_good))
p_values[100:200] = 0.01  # Simulate some significant p-values in a frequency band

# Create a figure with two subplots one above the other
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot the Power Spectral Density for both signals in the first subplot
ax1.plot(f_good, Pxx_good, label='Good Sleeper')
# ax1.semilogy(f_insomnia, Pxx_insomnia, label='Insomnia')
ax1.set_ylabel('EEG Power Spectral Density (uV^2/Hz)')
ax1.set_title('Simulated EEG Power Spectral Density')
ax1.legend()
ax1.set_xlim(0, 40)
ax1.yaxis.set_minor_locator(plt.NullLocator())  # Remove y-axis minor ticks
ax1.spines['top'].set_visible(False)  # Hide the top spine
ax1.spines['right'].set_visible(False)  # Hide the right spine
ax1.grid(False)

# Create the significance test plot in the second subplot
ax2.fill_between(f_good, p_values, alpha=0.3, color='gray', step='pre')
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('t-test p')
ax2.set_ylim(0, 0.1)
ax2.axhline(y=0.05, color='k', linestyle='--')  # Significance level line
ax2.invert_yaxis()  # Invert y axis for significance plot
ax2.grid(False)
ax2.spines['top'].set_visible(False)  # Hide the top spine
ax2.spines['right'].set_visible(False)  # Hide the right spine

# Adjust the layout so the subplots are close together
fig.tight_layout(pad=3.0)

plt.show()


