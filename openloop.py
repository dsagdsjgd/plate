import numpy as np

# 载入逆矩阵 npz 文件
data = np.load("H_inv_matrix.npz", allow_pickle=True)
frequencies = data["frequencies"]
G = data["H_inv"]  # shape (3,3), dtype=object，每个元素是复数数组

N = len(frequencies)
I = np.eye(3, dtype=np.complex128)  # 3x3单位阵

# 初始化结果矩阵，结构同G
result_matrix = [[np.zeros(N, dtype=np.complex128) for _ in range(3)] for _ in range(3)]

for k in range(N):
    # 构造频率点k的矩阵G_k
    G_k = np.array([[G[i][j][k] for j in range(3)] for i in range(3)], dtype=np.complex128)

    # 计算 -G_k + I
    res_k = -G_k + I

    # 赋值回 result_matrix
    for i in range(3):
        for j in range(3):
            result_matrix[i][j][k] = res_k[i, j]

result_matrix = np.array(result_matrix, dtype=object)

# 保存结果矩阵
np.savez("minus_G_plus_I.npz", frequencies=frequencies, M=result_matrix)
print("矩阵 -G + I 已保存为 minus_G_plus_I.npz")
1