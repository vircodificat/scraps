all: build/os1k.elf build/os1k.img

build/os1k.img: build/os1k.elf
	mkdir -p build
#	objcopy --dump-section .text=build/os1k.text.bin build/os1k.elf
#	objcopy --dump-section .rodata=build/os1k.rodata.bin build/os1k.elf
#	cat build/os1k.text.bin build/os1k.rodata.bin > build/os1k.bin
	objcopy -O binary build/os1k.elf build/os1k.bin

build/os1k.elf: kernel.c linker.ld syscalls.S sbi.h sbi.c
	mkdir -p build
	clang --target=riscv64-unknown-elf -static -nostdlib -mcmodel=medany -o build/os1k.elf -g kernel.c linker.ld syscalls.S sbi.c

clean:
	rm -rf build

.PHONY: clean
