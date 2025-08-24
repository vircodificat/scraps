all: build/os1k.elf

build/os1k.elf: kernel.c linker.ld syscalls.S sbi.h sbi.c
	mkdir -p build
	clang --target=riscv64-unknown-elf -static -nostdlib -mcmodel=medany -o build/os1k.elf -g kernel.c linker.ld syscalls.S sbi.c

clean:
	rm -rf build

.PHONY: clean
