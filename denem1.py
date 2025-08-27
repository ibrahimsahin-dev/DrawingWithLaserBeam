import pandas as pd
import numpy as np

# --- Configuration ---
# Your input file
input_filename = 'equal_coords_clean.csv'
# The cutoff ratio you requested
cutoff_ratio = 0.1


# --- Main Script ---
print(f"Processing {input_filename}...")

# 1. Load the coordinate data from the CSV file
# The file has no header, so we name the columns 'x' and 'y'.
try:
    df = pd.read_csv(input_filename, header=None, names=['x', 'y'])
    print(f"Successfully loaded {len(df)} coordinate points.")
except FileNotFoundError:
    print(f"ERROR: Could not find the file '{input_filename}'. Make sure it's in the same folder.")
    exit()

# 2. Center the shape and convert to complex numbers
# We find the average X and Y to find the center of your shape.
x_mean = df['x'].mean()
y_mean = df['y'].mean()

# We shift all points so the shape is centered at (0,0).
# This average value will be the 'offset' for your DAC later.
# Then, we convert the (x, y) pairs into complex numbers z = x + i*y.
z = (df['x'] - x_mean) + 1j * (df['y'] - y_mean)
N = len(z)

# 3. Calculate the Fast Fourier Transform (FFT)
# This is the core step that finds the 'recipe' of rotating circles for your shape.
# We normalize the FFT by dividing by the number of points (N).
fft_coeffs = np.fft.fft(z) / N

# 4. Sort and Filter the Coefficients
# The raw FFT output is tricky to work with, so we shift it so the
# most important, low-frequency coefficients are in the center of the array.
fft_coeffs_sorted = np.fft.fftshift(fft_coeffs)

# Now, we apply your cutoff_ratio to decide how many circles to use.
# A smaller number gives a smoother shape.
# M is the number of circles/coefficients to keep on each side of the center.
M = int(N * cutoff_ratio * 0.5)

print(f"\nTotal points (N): {N}")
print(f"The center of your shape is at (x, y): ({x_mean:.2f}, {y_mean:.2f})")
print(f"Cutoff ratio: {cutoff_ratio} -> Keeping {M} coefficients on each side of center.")
print(f"This will result in a C array with {2 * M} total coefficients.")

# We grab the 'M' coefficients from the left and right of the center.
zero_freq_index = N // 2
start_index = zero_freq_index - M
end_index = zero_freq_index + M + 1
filtered_coeffs_vals = fft_coeffs_sorted[start_index:end_index]
filtered_coeffs_n = np.arange(-M, M + 1)


# 5. Generate the C code snippet for the STM32
print("\n--- Copy the C Code below into your STM32 Project ---")

c_code = "const FourierCoefficient coeffs[] = {\n"
for n, c in zip(filtered_coeffs_n, filtered_coeffs_vals):
    # The n=0 component is the shape's center, which we handle with a DAC offset.
    # We only need the coefficients for the rotating vectors.
    if n == 0:
      continue
    # We can ignore tiny values that are just floating point noise.
    if np.abs(c) > 1e-4:
        c_code += f"    {{{n}, {c.real:.4f}f, {c.imag:.4f}f}},\n"

# Tidy up the end of the string
if c_code.endswith(",\n"):
    c_code = c_code[:-2] + "\n"
c_code += "};"
c_code += f"\nconst int num_coeffs = sizeof(coeffs) / sizeof(coeffs[0]);"

print(c_code)
