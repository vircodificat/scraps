#!/bin/bash

qemu_run="/home/$SUDO_USER/.local/qemu/bin/qemu-riscv64"
filename="disk.img"
image_size=64

set -e

if [[ "$EUID" != "0" ]]; then
    echo "Must be run as root"
    exit 1
fi

sudo_user="$SUDO_USER"
sudo_uid="$SUDO_UID"

set -x

dd if=/dev/zero of=${filename} bs=1M count=${image_size}
chown $sudo_user ${filename}

mkdir -p mnt
chown $sudo_user mnt

LOOP=$(losetup --show -f $filename)

parted \
    --script "$LOOP" \
    mklabel msdos \
    mkpart primary fat32 1MiB 32MiB \
    set 1 boot on \
    mkpart primary ext4 32MiB 100% \

mkfs.vfat -F 32 -n BOOT ${LOOP}p1
mkfs.ext4 -L rootfs ${LOOP}p2

mount ${LOOP}p1 mnt
cp build/Image mnt/
umount mnt

mount ${LOOP}p2 mnt

########################################

mkdir -p mnt/bin
mkdir -p mnt/sbin

rm -rf mnt/lost+found

#cp build/os1k.elf mnt/
#cp build/os1k.bin mnt/
cp build/init.cpio mnt/

cp build/busybox mnt/bin/
$qemu_run mnt/bin/busybox --install mnt/bin

#cat > mnt/sbin/init <<EOF
##!/bin/ash
#ash
#EOF
#chmod +x mnt/sbin/init

cd mnt
find .
cd ..

########################################

chown -R $sudo_user mnt

umount mnt
losetup -d $LOOP
