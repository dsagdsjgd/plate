import numpy as np
import matplotlib.pyplot as plt

# 读取两个文件，跳过表头
data1 = np.loadtxt('srs005.txt')
data2 = np.loadtxt('srs004.txt')

x1, y1 = data1[:, 0], data1[:, 1]
x2, y2 = data2[:, 0], data2[:, 1]

# 创建两个子图（2行1列）
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# 幅度图
ax1.plot(x1, y1, color='blue')
ax1.set_xscale('log')  # 设置x轴为对数刻度
ax1.set_ylabel('Magnitude')
ax1.set_title('Magnitude Response')
ax1.grid(True)

# 相位图
ax2.plot(x2, y2, color='red', linestyle='--')
ax2.set_xscale('log')  # 设置x轴为对数刻度
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Phase')
ax2.set_title('Phase Response')
ax2.grid(True)

# 自动调整布局
plt.tight_layout()
plt.show()
