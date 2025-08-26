#!/bin/bash

cd "$(dirname $(realpath $0))"

qemu-system-riscv64 \
    -nographic \
    -smp 1 \
    -machine virt \
    -m 1G \
    --no-reboot \
    -bios build/fw_jump.bin \
    -drive file=./disk.img,format=raw,id=hd0 \
    -kernel build/u-boot.bin \

#    -s -S \
#    -device virtio-mouse-pci,bus=pcie.0 \
#    -device virtio-net-device,netdev=net0 \
#    -netdev user,id=net0 \
#    -kernel build/u-boot.bin \
#    -initrd build/init.cpio \
#    -append "init=/sbin/init" \
#    -kernel build/Image \
#    -kernel hello.txt \
#    -initrd hello.txt \
#    -display none \
#    -serial mon:stdio \
#    -serial pty \
