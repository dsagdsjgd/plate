.PHONY: complexfile inter clean
INTER_FILES = \
	interpolated_data/2-1.csv \
	interpolated_data/2-2.csv \
	interpolated_data/3-3.csv \
	interpolated_data/3-1.csv

# === 原功能：生成 complex 文件夹中的复数传递函数 ===
complexfile:
	@echo "正在生成 complex 文件夹中的复数传递函数..."
	@for i in 1 2 3; do \
		for j in 1 2 3; do \
			python3 get_complex.py $$i $$j; \
		done \
	done

# === 插值处理：生成 interpolated_data 中的文件 ===
inter: $(INTER_FILES)
interpolated_data/%.csv: complex/%.csv complex/1-1.csv interpolate.py
	@echo "Interpolating $* ..."
	@mkdir -p interpolated_data
	@python3 inter.py $* complex interpolated_data

# === 清理（不破坏 interpolate.py 和 get_complex.py）===
clean:
	rm -rf complex interpolated_data
