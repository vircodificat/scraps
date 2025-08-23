#!/bin/bash


qemu-system-riscv64 \
    -machine virt \
    -nographic \
    -kernel build/Image \
    -initrd build/init.cpio \
    -s -S
