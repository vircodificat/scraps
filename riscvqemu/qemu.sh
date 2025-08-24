#!/bin/bash


qemu-system-riscv64 \
    -nographic \
    -smp 1 \
    -machine virt \
    -m 1G \
    --no-reboot \
    -dtb virt.dtb \
    -kernel build/os1k.elf

#    -kernel build/u-boot.bin \
#    -initrd build/init.cpio \
#    -append "init=/sbin/init" \
#    -kernel build/Image \
#    -kernel hello.txt \
#    -initrd hello.txt \
#    -display none \
#    -serial mon:stdio \
#    -serial pty \
