import numpy as np

def load_H_matrix(file_path):
    """
    加载 H_matrix.npz 文件，返回 frequencies 和 H_matrix
    H_matrix 是 3x3 矩阵，每个元素是一个长度为 freq_count 的复数数组
    """
    data = np.load(file_path, allow_pickle=True)
    frequencies = data["frequencies"]
    H_matrix = data["H"]
    return frequencies, H_matrix

def get_H0():
    return 4000 * np.eye(3)

def get_H1():
    l_2 = 0.09
    return np.array([
        [1, -l_2, 0],
        [1, l_2 / 2, np.sqrt(3) * l_2 / 2],
        [1, l_2 / 2, -np.sqrt(3) * l_2 / 2]
    ])

def get_H3():
    l = 0.024654
    return np.array([
        [1, 1, 1],
        [-l, l / 2, l / 2],
        [0, np.sqrt(3) * l / 2, -np.sqrt(3) * l / 2]
    ])

def get_H4():
    return 0.0075 * np.eye(3)

def get_H5():
    return (1 / 3360) * np.eye(3)

def get_H6(s):
    return np.array([
        [-25 - 3 / s - 100 / (1 + 1000 / s), 0, 0],
        [0, -30 - 3 / s - 100 / (1 + 1000 / s), 0],
        [0, 0, -25 - 3 / s - 100 / (1 + 1000 / s)]
    ])

def get_H7():
    return 3278 * np.eye(3)

def solve_for_frequency_point(H_matrix, freq_index, frequencies):
    """
    对给定频率点索引 freq_index，使用三组输入数据求解完整的传递函数矩阵 H_transfer，并返回中间变量 X, F
    """
    H0 = get_H0()
    H1 = get_H1()

    f_test = frequencies[freq_index]
    w = 2 * np.pi * f_test
    s = 1j * w

    H3 = get_H3()
    H4 = get_H4()
    H5 = get_H5()
    H6_mat = get_H6(s)
    H7 = get_H7()

    D = H5 @ H6_mat @ H7 @ H4 @ H3

    X = np.zeros((3, 3), dtype=np.complex128)
    F = np.zeros((3, 3), dtype=np.complex128)

    for j in range(3):
        y = np.zeros((3, 1), dtype=np.complex128)
        for i in range(3):
            hij = np.array(H_matrix[i][j], dtype=np.complex128)
            y[i, 0] = hij[freq_index]

        e_j = np.zeros((3, 1), dtype=np.complex128)
        e_j[j, 0] = 1

        try:
            x_j = np.linalg.solve(H0 @ H1, y - e_j)
        except np.linalg.LinAlgError:
            x_j = np.linalg.pinv(H0 @ H1) @ (y - e_j)

        f_j = D @ y

        X[:, j] = x_j.flatten()
        F[:, j] = f_j.flatten()

    try:
        H_transfer = X @ np.linalg.pinv(F)
    except np.linalg.LinAlgError:
        H_transfer = np.zeros((3, 3), dtype=np.complex128)

    return H_transfer, X, F


def main():
    global frequencies
    file_path = "H_matrix.npz"
    frequencies, H_matrix = load_H_matrix(file_path)

    freq_count = len(frequencies)
    transfer_functions = np.zeros((freq_count, 3, 3), dtype=np.complex128)

    X_all = np.zeros((freq_count, 3, 3), dtype=np.complex128)
    F_all = np.zeros((freq_count, 3, 3), dtype=np.complex128)

    for idx in range(freq_count):
        H_transfer, X, F = solve_for_frequency_point(H_matrix, idx, frequencies)
        transfer_functions[idx] = H_transfer
        X_all[idx] = X
        F_all[idx] = F

    dummy_results = np.zeros((freq_count, 6), dtype=np.complex128)
    np.savez("calculation_results.npz",
             frequencies=frequencies,
             results=dummy_results)

    T = np.empty((3, 3), dtype=object)
    for i in range(3):
        for j in range(3):
            T[i, j] = transfer_functions[:, i, j]

    np.savez("transfer_functions.npz",
             frequencies=frequencies,
             H=T)

    # 分开保存 X 和 F
    X = np.empty((3, 3), dtype=object)
    for i in range(3):
        for j in range(3):
            X[i, j] = X_all[:, i, j]
    np.savez("X_matrices.npz",
             frequencies=frequencies,
             H=X)
    F = np.empty((3, 3), dtype=object)
    for i in range(3):
        for j in range(3):
            F[i, j] = F_all[:, i, j]
    np.savez("F_matrices.npz",
             frequencies=frequencies,
             H=F)

    print("所有计算完成：")
    print("  - 传递函数矩阵保存至 transfer_functions.npz")
    print("  - X 保存至 X_matrices.npz")
    print("  - F 保存至 F_matrices.npz")


if __name__ == "__main__":
    main()
