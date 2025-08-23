#!/bin/bash

set -xe

mkdir -p build
mkdir -p sysroot

git clone $REPOS/linux --depth=1 --branch=v6.16
cd linux

export ARCH=riscv
export CROSS_COMPILE=riscv64-linux-gnu-

make tinyconfig

cd ..

cp linux/.config .config
cp .config .config.tiny
patch -p0 < config.diff
cp .config linux/
cd linux

make -j
make -j vmlinux

ls \
    arch/riscv/boot/Image \
    arch/riscv/boot/Image.xz \
    vmlinux

cp arch/riscv/boot/Image ../build/.
cp arch/riscv/boot/Image.xz ../build/.
cp vmlinux ../build/.

cd ..

riscv64-linux-gnu-gcc -static -o sysroot/sbin/init init.c

cd sysroot

find . | cpio -o -H newc > ../build/init.cpio
