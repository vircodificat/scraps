void panic(void);
void halt(void);
void kernel_main(void);
//void putchar(char ch);
void _putchar(char ch);
//void puts(const char *s);
//struct sbiret sbi_call(long arg0, long arg1, long arg2, long arg3, long arg4, long arg5, long fid, long eid);
//struct sbiret _putchar(char ch);


#define LEGACY_CONSOLE_PUTCHAR 1

// DBCN is the Debug Console EID
#define DBCN 0x4442434E

#define DBCN_CONSOLE_WRITE      0
#define DBCN_CONSOLE_READ       1
#define DBCN_CONSOLE_WRITE_BYTE 2

struct sbiret {
    long error;
    long value;
};

extern char __kernel_base[];
extern char __stack_top[];
extern char __bss[], __bss_end[];
extern char __free_ram[], __free_ram_end[];
extern char _binary_shell_bin_start[], _binary_shell_bin_size[];


__attribute__((section(".text.boot")))
__attribute__((naked))
void boot(void) {
    __asm__ __volatile__(
        "mv sp, %[stack_top]\n"
        "j kernel_main\n"
        :
        : [stack_top] "r" (__stack_top)
    );
}

void kernel_main(void) {
    _putchar('!');
    halt();
}

void panic(void) {
    __asm__ __volatile__("wfi");
    for (;;) { ; }
}

void halt(void) {
    __asm__ __volatile__("wfi");
    for (;;) { ; }
}

/*
void puts(const char *s) {
    while (*s) {
        putchar(*s);
        s++;
    }
}
*/

/*
struct sbiret putchar(char ch) {
    return sbi_call(
        ch,     // a0
        0,      // a2 (unused)
        0,      // a3 (unused)
        0,      // a4 (unused)
        0,      // a5 (unused)
        0,      // a6 (unused)
        0,      // FID
        LEGACY_CONSOLE_PUTCHAR    // EID
    );
    return sbi_call(
        ch,     // a0
        0,      // a2 (unused)
        0,      // a3 (unused)
        0,      // a4 (unused)
        0,      // a5 (unused)
        0,      // a6 (unused)
        DBCN_CONSOLE_WRITE_BYTE,      // FID = sbi_debug_console_write_byte
        DBCN    // EID = DBCN (DeBug CoNsole)
    );
}
*/

/*
struct sbiret sbi_call(
    long arg0,
    long arg1,
    long arg2,
    long arg3,
    long arg4,
    long arg5,
    long fid,
    long eid
) {
    register long a0 __asm__("a0") = arg0;
    register long a1 __asm__("a1") = arg1;
    register long a2 __asm__("a2") = arg2;
    register long a3 __asm__("a3") = arg3;
    register long a4 __asm__("a4") = arg4;
    register long a5 __asm__("a5") = arg5;
    register long a6 __asm__("a6") = fid;
    register long a7 __asm__("a7") = eid;

    __asm__ __volatile__(
        "ecall"
        :
        "=r"(a0),
        "=r"(a1)
        :
        "r"(a0),
        "r"(a1),
        "r"(a2),
        "r"(a3),
        "r"(a4),
        "r"(a5),
        "r"(a6),
        "r"(a7)
        :
        "memory"
    );
    return (struct sbiret){.error = a0, .value = a1};
}
*/
