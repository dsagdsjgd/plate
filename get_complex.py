import sys
import os
import numpy as np

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    data_lines = [line.strip() for line in lines if line.strip() and line.strip()[0].isdigit()]
    freqs = []
    values = []
    for line in data_lines:
        parts = line.split()
        freqs.append(float(parts[0]))
        values.append(float(parts[1]))
    return np.array(freqs), np.array(values)

def convert_to_complex(mag_db, phase_deg):
    mag = 10 ** (mag_db / 20)
    phase_rad = np.deg2rad(phase_deg)
    return mag * np.exp(1j * phase_rad)

def main(i, j):
    mag_file = f"new_transfer/{i}-{j}幅度.txt"
    phase_file = f"new_transfer/{i}-{j}相位.txt"
    output_dir = "complex"
    output_file = f"{output_dir}/{i}-{j}.csv"  # 修改为 CSV

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    freq1, mag = read_file(mag_file)
    freq2, phase = read_file(phase_file)

    if not np.allclose(freq1, freq2):
        print("频率不匹配")
        sys.exit(1)

    complex_values = convert_to_complex(mag, phase)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Frequency(Hz),Real,Imaginary\n")  # 写入表头
        for freq, val in zip(freq1, complex_values):
            f.write(f"{freq:.6e},{val.real:.6e},{val.imag:.6e}\n")

    print(f"转换完成: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
