.PHONY: run

run: build/main
	build/main

build/main: main.c
	mkdir -p build
	gcc main.c -lasound -lm -o build/main
