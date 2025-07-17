import numpy as np
import pandas as pd

"""
file_matrix = np.array([
    ["interpolated_data/3-3.csv", "complex/3-2.csv","complex/3-2.csv",],
    ["complex/3-2.csv",        "interpolated_data/3-3.csv", "complex/3-2.csv",],
    ["complex/3-2.csv",          "complex/3-2.csv",          "interpolated_data/3-3.csv",]
], dtype=object)
"""

file_matrix = np.array([
    ["complex/1-1.csv", "complex/1-2.csv", "complex/1-3.csv"],
    ["interpolated_data/2-1.csv",          "interpolated_data/2-2.csv", "complex/2-3.csv"],
    ["interpolated_data/3-1.csv",          "complex/3-2.csv",           "interpolated_data/3-3.csv"]
], dtype=object)


# file_matrix = np.load("file_matrix.npy", allow_pickle=True)


def load_complex(filepath):
    df = pd.read_csv(filepath)
    freq = df['Frequency(Hz)'].values
    real = df['Real'].values
    imag = df['Imaginary'].values
    return freq, real + 1j * imag


H_matrix = [[None for _ in range(3)] for _ in range(3)]
frequencies = None

for i in range(3):
    for j in range(3):
        path = file_matrix[i][j]
        print(f"Loading: {path}")
        freq, cval = load_complex(path)

        if frequencies is None:
            frequencies = freq
        else:
            if not np.allclose(frequencies, freq):
                raise ValueError(f"Frequency mismatch in {path}")

        H_matrix[i][j] = cval

H_matrix = np.array(H_matrix, dtype=object)
print("原始矩阵加载完成。开始计算逆矩阵...")


N = len(frequencies)
H_inv_matrix = [[np.zeros(N, dtype=np.complex128) for _ in range(3)] for _ in range(3)]

for k in range(N):
    H_k = np.array([[H_matrix[i][j][k] for j in range(3)] for i in range(3)], dtype=np.complex128)
    try:
        H_k_inv = np.linalg.inv(H_k)
    except np.linalg.LinAlgError:
        H_k_inv = np.full((3, 3), np.nan + 1j * np.nan)
    for i in range(3):
        for j in range(3):
            H_inv_matrix[i][j][k] = H_k_inv[i, j]

H_inv_matrix = np.array(H_inv_matrix, dtype=object)
print("逆矩阵计算完成。开始计算 -G + I 矩阵...")

I = np.eye(3, dtype=np.complex128)
minus_G_plus_I = [[np.zeros(N, dtype=np.complex128) for _ in range(3)] for _ in range(3)]

for k in range(N):
    G_k = np.array([[H_inv_matrix[i][j][k] for j in range(3)] for i in range(3)], dtype=np.complex128)
    M_k = -G_k + I
    for i in range(3):
        for j in range(3):
            minus_G_plus_I[i][j][k] = M_k[i, j]

minus_G_plus_I = np.array(minus_G_plus_I, dtype=object)


np.savez("H_matrix.npz", frequencies=frequencies, H=H_matrix)
print("原始矩阵已保存为 H_matrix.npz")

np.savez("H_inv_matrix.npz", frequencies=frequencies, H_inv=H_inv_matrix)
print("逆矩阵已保存为 H_inv_matrix.npz")

np.savez("minus_G_plus_I.npz", frequencies=frequencies, M=minus_G_plus_I)
print("矩阵 -G + I 已保存为 minus_G_plus_I.npz")

# 可选：保存路径矩阵，供以后更改
np.save("file_matrix.npy", file_matrix)
