#!/bin/bash


qemu-system-riscv64 \
    -nographic \
    -machine virt \
    -m 1G \
    -kernel build/os1k.elf \
    -s -S

#    -bios build/fw_payload.bin \
#    -kernel build/u-boot.bin \
#    -initrd build/init.cpio \
#    -append "init=/sbin/init" \
#    -kernel build/Image \
#    -kernel hello.txt \
#    -initrd hello.txt \
#    -display none \
#    -serial mon:stdio \
#    -serial pty \
