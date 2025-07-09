.PHONY: complexfile

complexfile:
	@echo "正在生成 complex 文件夹中的复数传递函数..."
	@for i in 1 2 3; do \
		for j in 1 2 3; do \
			python3 get_complex.py $$i $$j; \
		done \
	done
clean:
	rm -rf complex     