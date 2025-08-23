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
