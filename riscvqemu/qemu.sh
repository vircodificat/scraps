#!/bin/bash

cd "$(dirname $(realpath $0))"

qemu-system-riscv64 \
    -nographic \
    -smp 2 \
    -machine virt \
    -m 8G \
    --no-reboot \
    -device virtio-net-device,netdev=net0 \
    -netdev user,id=net0 \
    -bios build/fw_jump.bin \
    -kernel build/u-boot.bin \
    -drive file=disk.img,format=raw,id=hd1 \

#    -s -S \
#    -object rng-random,id=rng0,filename=/dev/urandom \
#    -device virtio-rng-pci,rng=rng0 \
#    -drive file=debian_install.img,format=raw,id=hd0 \
#    -drive file=~/Downloads/debian-13.0.0-riscv64-DVD-1.iso,format=raw,id=hd1 \
#    -kernel build/Image \
#    -append "init=/bin/sh root=/dev/vda2 rw" \
#    -device virtio-net-device,netdev=net0 \
#    -netdev user,id=net0 \
#    -device virtio-mouse-pci,bus=pcie.0 \
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
#    -append "init=/bin/sh root=/dev/vda2" \
#    -nographic \
