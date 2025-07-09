import numpy as np
import matplotlib.pyplot as plt
import os

# === 配置 ===
target_file = "2-1.txt"                     # 需要插值的目标文件
target_path = os.path.join("complex", target_file)
reference_path = os.path.join("complex", "1-1.txt")  # 作为频率参考的文件
output_dir = "interpolated_data"
os.makedirs(output_dir, exist_ok=True)

# === 工具函数 ===
def load_data(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        freq = np.array([float(x) for x in lines[0].strip().split()])
        real = np.array([float(x) for x in lines[1].strip().split()])
        imag = np.array([float(x) for x in lines[2].strip().split()])
    return freq, real, imag

def save_data(filepath, freq, real, imag):
    with open(filepath, 'w') as f:
        f.write(" ".join(f"{x:.6f}" for x in freq) + "\n")
        f.write(" ".join(f"{x:.6f}" for x in real) + "\n")
        f.write(" ".join(f"{x:.6f}" for x in imag) + "\n")

# === 读取数据 ===
std_freq, _, _ = load_data(reference_path)
raw_freq, raw_real, raw_imag = load_data(target_path)

# === 插值 ===
interp_real = np.interp(std_freq, raw_freq, raw_real)
interp_imag = np.interp(std_freq, raw_freq, raw_imag)

# === 保存结果 ===
output_txt = os.path.join(output_dir, target_file)
save_data(output_txt, std_freq, interp_real, interp_imag)

# === 绘图比较 ===
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(raw_freq, raw_real, 'bo-', label='原始实部')
plt.plot(std_freq, interp_real, 'r.--', label='插值实部')
plt.xlabel("频率")
plt.ylabel("实部")
plt.title(f"{target_file} - 实部对比")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(raw_freq, raw_imag, 'bo-', label='原始虚部')
plt.plot(std_freq, interp_imag, 'r.--', label='插值虚部')
plt.xlabel("频率")
plt.ylabel("虚部")
plt.title(f"{target_file} - 虚部对比")
plt.legend()

plt.tight_layout()
output_png = os.path.join(output_dir, target_file.replace(".txt", "_compare.png"))
plt.savefig(output_png)
plt.close()

