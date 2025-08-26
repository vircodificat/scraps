#!/bin/bash

set -xe

LINUX_COMMIT=v6.16
BUSYBOX_COMMIT=1_34_stable
UBOOT_COMMIT=v2025.04
OPENSBI_COMMIT=v1.7

source build.env.sh

cd "$(dirname "${BASH_SOURCE[0]}")"

mkdir -p build

ls $(which "$CROSS_COMPILE-gcc") # ensure gcc exists

function download_git_repos() {
    if [ ! -d linux ]; then
        url="https://github.com/torvalds/linux"
        git clone $url --depth=1 --branch=$LINUX_COMMIT --filter=blob:none
    else
        git -C linux   checkout $LINUX_COMMIT
    fi

    if [ ! -d busybox ]; then
        url="https://git.busybox.net/busybox"
        git clone $url --depth=1 --branch=$BUSYBOX_COMMIT --filter=blob:none
    else
        git -C busybox checkout $BUSYBOX_COMMIT
    fi

    if [ ! -d u-boot ]; then
        url="https://github.com/u-boot/u-boot"
        git clone $url --depth=1 --branch=$UBOOT_COMMIT --filter=blob:none
    else
        git -C u-boot  checkout $UBOOT_COMMIT
    fi

    if [ ! -d opensbi ]; then
        url="https://github.com/riscv-software-src/opensbi"
        git clone $url --depth=1 --branch=$OPENSBI_COMMIT --filter=blob:none
    else
        git -C opensbi checkout $OPENSBI_COMMIT
    fi
}

function build_linux() {
    cd linux

    make defconfig
#    patch -p0 < ../configs/linux.config.diff
    make -j 10
    make -j 10 vmlinux

    cp \
        arch/riscv/boot/Image \
        vmlinux \
        ../build/

    cd ..
}

function build_busybox() {
    cp configs/busybox.config busybox/.config

    cd busybox

    make -j

    cp \
        busybox \
        busybox_unstripped \
        ../build/

    cd ..
}

function build_uboot() {
    cp configs/u-boot.config u-boot/.config
    cd u-boot

#    make qemu-riscv64_smode_defconfig
    make -j

    cp \
        u-boot \
        u-boot.bin \
        ../build/

    cd ..
}

function build_opensbi() {
    cd opensbi

    make PLATFORM=generic FW_TEXT_START=0x80000000 -j10

    cp \
        build/platform/generic/firmware/fw_payload.elf \
        build/platform/generic/firmware/fw_payload.bin \
        build/platform/generic/firmware/fw_dynamic.elf \
        build/platform/generic/firmware/fw_dynamic.bin \
        build/platform/generic/firmware/fw_jump.elf \
        build/platform/generic/firmware/fw_jump.bin \
        ../build/

    cd ..
}

function build_os1k() {
    cd os1k

    make

    cp \
        build/os1k.elf \
        build/os1k.bin \
        ../build/

    cd ..
}

function build_sysroot() {
    mkdir -p sysroot
    cd sysroot
    find .
    find . | cpio -o -H newc > ../build/init.cpio
    cd ..
}

download_git_repos
build_linux
build_busybox
build_uboot
build_opensbi
build_os1k
build_sysroot
