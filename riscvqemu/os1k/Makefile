all: os1k.elf

os1k.elf: kernel.c linker.ld
	mkdir -p build
	clang --target=riscv64-unknown-elf -static -nostdlib -mcmodel=medany -o build/os1k.elf -g kernel.c linker.ld

clean:
	rm -rf build

.PHONY: clean
