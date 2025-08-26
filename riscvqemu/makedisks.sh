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
    mkpart primary ext4 1MiB 100% \
    set 1 boot on

# This apparently removes support for features U-Boot doesn't work with:
# -O ^64bit,^metadata_csum,^bigalloc
mkfs.ext4 -O ^64bit,^metadata_csum,^bigalloc ${LOOP}p1

mount ${LOOP}p1 mnt

########################################

mkdir -p mnt/bin
mkdir -p mnt/sbin

rm -rf mnt/lost+found

cp build/Image mnt/
cp virt.dtb mnt/
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
