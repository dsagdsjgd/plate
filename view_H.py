import numpy as np
import matplotlib.pyplot as plt

# 加载
data = np.load("H_matrix.npz", allow_pickle=True)
frequencies = data["frequencies"]
H_matrix = data["H"]

# 画图
plt.figure(figsize=(15, 10))
for i in range(3):
    for j in range(3):
        plt.subplot(3, 3, i * 3 + j + 1)
        
        hij = np.array(H_matrix[i][j], dtype=np.complex128)
        print(type(hij)) 
        mag_db = 20 * np.log10(np.abs(hij))  # dB 幅度

        plt.semilogx(frequencies, mag_db, 'b')
        plt.title(f"$H_{{{i+1}{j+1}}}$")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude (dB)")
        plt.grid(True)

plt.tight_layout()
plt.suptitle("Frequency Response Magnitude (dB) of Each $H_{ij}$", fontsize=16, y=1.02)
plt.show()
