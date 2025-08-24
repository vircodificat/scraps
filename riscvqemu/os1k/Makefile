all: build/os1k.elf

build/os1k.elf: kernel.c linker.ld syscalls.S
	mkdir -p build
	clang --target=riscv64-unknown-elf -static -nostdlib -mcmodel=medany -o build/os1k.elf -g kernel.c linker.ld syscalls.S

clean:
	rm -rf build

.PHONY: clean
