import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# 加载数据
data = np.load("minus_G_plus_I.npz", allow_pickle=True)
frequencies = data["frequencies"]
H_matrix = data["M"]

# 创建 PDF 文件
with PdfPages("response_plots.pdf") as pdf:

    # 幅度图
    plt.figure(figsize=(15, 10))
    for i in range(3):
        for j in range(3):
            plt.subplot(3, 3, i * 3 + j + 1)
            hij = np.array(H_matrix[i][j], dtype=np.complex128)
            mag_db = 20 * np.log10(np.abs(hij))
            plt.semilogx(frequencies, mag_db, 'b')
            plt.title(f"$H_{{{i+1}{j+1}}}$ Magnitude")
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Magnitude (dB)")
            plt.grid(True)
    plt.tight_layout()
    plt.suptitle("Frequency Response Magnitude (dB) of Each $H_{ij}$", fontsize=16, y=1.02)
    pdf.savefig()  # 保存这一页
    plt.close()

    # 相位图
    plt.figure(figsize=(15, 10))
    for i in range(3):
        for j in range(3):
            plt.subplot(3, 3, i * 3 + j + 1)
            hij = np.array(H_matrix[i][j], dtype=np.complex128)
            phase_deg = np.angle(hij, deg=True)
            plt.semilogx(frequencies, phase_deg, 'r')
            plt.title(f"$H_{{{i+1}{j+1}}}$ Phase")
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Phase (°)")
            plt.grid(True)
    plt.tight_layout()
    plt.suptitle("Frequency Response Phase (°) of Each $H_{ij}$", fontsize=16, y=1.02)
    pdf.savefig()  # 保存这一页
    plt.close()

print("PDF 文件已保存为 response_plots.pdf")
