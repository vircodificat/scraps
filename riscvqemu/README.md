# Linux in RISC-V

First, we build the Linux kernel.
We take inspiration from https://www.youtube.com/watch?v=u2Juz5sQyYQ
See build.sh
The key difference is setting these environment variables:

```console
export ARCH=riscv
export CROSS_COMPILE=riscv64-linux-gnu-
```

and that the RISC-V arch has slightly different configuration options.
Note that config.diff is used to handle the `make menuconfig`.

We also build a small `init` file at `src/init.c`.
This gets packaged into `build/init.cpio`.

We then run the emulator with `./qemu.sh`.
The `-kernel` flag loads `build/Image` at the standard kernel address `0x8020_0000`.
The `-initrd` flag loads the `build/init.cpio` file at `0x84200000` (I think).
(The device tree seems to live at `0x87e00000`).
(Or is it `0xbfe00000` when passed with `-dtb`).


DON'T FORGET YOU CAN EXIT QEMU WITH: `Ctrl+A X`

By passing `-s` and `-S` (both lower and caps) to QEMU,
we tell QEMU to suspend before execution and wait for `gdb` to connect.

We add a `gdbinit` file to ease working with this.
This will remotely connect to QEMU, set the architecture to RV64, and set a few nice breakpoints.
We can run it with `./gdb.sh`.
Note that we need `gdb-multiarch` installed, since we are working with RISC-V, not x86_64.

## OS1k

When I couldn't get Linux or U-Boot to boot, I tried a smoke test using a stripped down version of this blog post:

https://operating-system-in-1000-lines.vercel.app

See `os1k`.

## Device Tree

You can dump the device tree for QEMU `virt` with:

```console
$ qemu-system-riscv64 \
  -machine virt \
  -m 1G \
  -nographic \
  -machine dumpdtb=virt.dtb
```

You can then decompile it with:

```console
$ dtc -I dtb -O dts virt.dtb > virt.dts
```

## GDB Tips

You can list the (hardware) threads with `info threads`.

You can switch which thread receives commands with `thread N`.
HOWEVER -- the threads are 1-indexed, NOT 0-indexed(!!!)

You can switch to the source view with `layout src`.
The up and down *arrow* keys scroll through the viewport.
However, you can't copy and paste in this mode for some stupid reason.
And you can't get out of this mode by running any command
(at least, none that I've found).
You get out by the hotkey `Ctrl-x a`
(Annoyingly close to `Ctrl-a x` to quit in QEMU).

## OpenSBI

[SBI](https://drive.google.com/file/d/1RHY5Gj0cDSrY5BlK6pGblZt03fDRF2-g/view), or Supervisor Binary Interface,
is the equivalent of BIOS for RISC-V.
The standard implementation is called OpenSBI: https://github.com/riscv-software-src/opensbi

I'm mostly following along with the following guide:

https://popovicu.com/posts/risc-v-sbi-and-full-boot-process/

OpenSBI loads at `0x8000_0000` (the start of physical RAM in most systems)
and eventually dispatches to the operating system kernel, starting at `0x8020_0000`.
It starts off in M-mode, but drops into S-mode before doing so.

It seems the system is meant to supply the following to SBI:

* the hartid in `a0`
* a pointer to the device tree in `a1`

Then, SBI sets up the `mtvec` so that it can respond to `ecall`s from the kernel.
These provide basic BIOS functionality, such as a debug console (DBCN) and system reset (SRST).
(I thought it was cute that the value of the Extension ID (EID), such as DBCN,
is given the hex value of the ASCII bytes that spell out the command.
Very cool!

When you run `qemu-system-riscv64`, the default behavior is to bring up the system using an built-in version of OpenSBI.
You can use the `-bios` flag to replace it with a different bios firmware.


## U-Boot

Some useful U-Boot commands:

`bdinfo` prints the board information.

`ls virtio 0:1` will list the files on device 0 partition 1 of the virtio bus.
`load virtio 0:1 0x80200000 /hello.txt` will load `hello.txt` at the address `0x80200000`.

`md.b 0x80200000 0x40` will read (memory display).
`mw.b 0x80200007 0x0` will write to the memory.

`fdt print` and `fdt addr` print the device tree and give its address in memory.
Note that there is an environment variable `$fdt_addr_r`
which represents the address where the DT is expected to be loaded during boot.
We can use `fdt addr ${fdt_addr_r}` to place it there.

`cls` clears the screen.

See `run.txt` for a few U-Boot command snippets useful for booting.

For some reason, I can get `saveenv` to save the environment to disk,
but I can't get it to load.
I get an error `** Bad device specification virtio 0 **`.

I managed to boot the Debian installer and the Debian installation.
The trick is to use `bootefi` and to be mindful of the partitions.
(It seemed like I needed to ensure that the first virtio block device was the installer).


## Extra

* https://risc-v-machines.readthedocs.io/en/latest/linux/simple/
* https://docs.u-boot.org/en/latest/learn/talks.html
* https://github.com/mit-pdos/xv6-riscv
* https://blog.stephenmarz.com/
* https://docs.oasis-open.org/virtio/virtio/v1.1/virtio-v1.1.pdf
