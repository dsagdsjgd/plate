import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os
import sys

# === 命令行参数 ===
if len(sys.argv) != 4:
    print("Usage: python interpolate.py <basename> <input_dir> <output_dir>")
    sys.exit(1)

basename = sys.argv[1]  # 如 "2-1"
input_dir = sys.argv[2]
output_dir = sys.argv[3]

target_file = f"{basename}.csv"
target_path = os.path.join(input_dir, target_file)
reference_path = os.path.join(input_dir, "1-1.csv")
os.makedirs(output_dir, exist_ok=True)

# === 读取CSV数据 ===
def load_csv(filepath):
    df = pd.read_csv(filepath)
    freq = df['Frequency(Hz)'].values
    real = df['Real'].values
    imag = df['Imaginary'].values
    return freq, real, imag

def save_data(filepath, freq, real, imag):
    df_out = pd.DataFrame({
        'Frequency(Hz)': freq,
        'Real': real,
        'Imaginary': imag
    })
    df_out.to_csv(filepath, index=False, float_format='%.6f')

# === 读取数据 ===
std_freq, _, _ = load_csv(reference_path)
raw_freq, raw_real, raw_imag = load_csv(target_path)

# === 构造复数数据进行插值 ===
raw_complex = raw_real + 1j * raw_imag
interp_func = interp1d(raw_freq, raw_complex, kind='linear', bounds_error=False, fill_value="extrapolate")
interp_complex = interp_func(std_freq)

# === 拆解、保存 ===
interp_real = interp_complex.real
interp_imag = interp_complex.imag
output_csv = os.path.join(output_dir, target_file)
save_data(output_csv, std_freq, interp_real, interp_imag)


# === 绘图比较 ===
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.semilogx(raw_freq, raw_real, 'bo-', label='raw real part')
plt.semilogx(std_freq, interp_real, 'r.--', label='interpolated real part') 
plt.xlabel("Frequency (Hz)")
plt.ylabel("Real Part")
plt.title(f"{target_file} - Real Part Comparison")
plt.legend()

plt.subplot(1, 2, 2)
plt.semilogx(raw_freq, raw_imag, 'bo-', label='raw imaginary part')
plt.semilogx(std_freq, interp_imag, 'r.--', label='interpolated imaginary part')
plt.xlabel("Frequency (Hz)")
plt.ylabel("Imaginary Part")
plt.title(f"{target_file} - Imaginary Part Comparison")
plt.legend()

plt.tight_layout()
#plt.savefig(os.path.join(output_dir, target_file.replace(".csv", "_compare.png")))
plt.close()
