import numpy as np
import pandas as pd
import os

complex_dir = "complex"
interpolated_dir = "interpolated_data"


H_matrix = [[None for _ in range(3)] for _ in range(3)]
frequencies = None  # 用于检查频率一致性

def load_complex(filepath):
    df = pd.read_csv(filepath)
    freq = df['Frequency(Hz)'].values
    real = df['Real'].values
    imag = df['Imaginary'].values
    complex_vals = real + 1j * imag
    return freq, complex_vals

for i in range(1, 4):
    for j in range(1, 4):
        fname = f"{i}-{j}.csv"
        interp_path = os.path.join(interpolated_dir, fname)
        orig_path = os.path.join(complex_dir, fname)

        if os.path.exists(interp_path):
            print(f"Using interpolated: {interp_path}")
            freq, cval = load_complex(interp_path)
        elif os.path.exists(orig_path):
            print(f"Using original: {orig_path}")
            freq, cval = load_complex(orig_path)
        else:
            raise FileNotFoundError(f"Neither {interp_path} nor {orig_path} exists.")

        if frequencies is None:
            frequencies = freq
        else:
            if not np.allclose(frequencies, freq):
                raise ValueError(f"Frequency mismatch in {fname}")

        H_matrix[i-1][j-1] = cval
print(H_matrix)
# 可选：保存为 npz 文件
np.savez("H_matrix.npz", frequencies=frequencies, H=np.array(H_matrix, dtype=object))
print("矩阵 H 已保存为 H_matrix.npz")
