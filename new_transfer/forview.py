import numpy as np
import matplotlib.pyplot as plt

def load_data(filepath):
    freqs = []
    values = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    freq = float(parts[0])
                    val = float(parts[1])
                    freqs.append(freq)
                    values.append(val)
                except ValueError:
                    continue  # 忽略无法解析的行
    return np.array(freqs), np.array(values)

magnitude_file = r"2-1幅度.txt"
phase_file = r"2-1相位.txt"

# 读取数据
freqs_mag, mags_db = load_data(magnitude_file)
freqs_phase, phases_deg = load_data(phase_file)

# 检查频率一致性
if not np.allclose(freqs_mag, freqs_phase):
    raise ValueError("频率点不一致，请检查文件内容！")

# 绘图
plt.figure(figsize=(12, 6))

# 幅频图
plt.subplot(2, 1, 1)
plt.semilogx(freqs_mag, mags_db, 'b-')
plt.title("Bode Plot")
plt.ylabel("Magnitude (dB)")
plt.grid(True, which='both')

# 相频图
plt.subplot(2, 1, 2)
plt.semilogx(freqs_phase, phases_deg, 'g-')
plt.xlabel("Frequency (Hz)")
plt.ylabel("Phase (degrees)")
plt.grid(True, which='both')

plt.tight_layout()
plt.show()
