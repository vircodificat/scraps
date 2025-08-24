#include "sbi.h"

void panic(void);
void halt(void);
void kernel_main(void);
void _putchar(char ch);


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
    struct sbiret result;
    result = sbi_get_impl_version();
    result = sbi_probe_extension(DBCN);
    result = sbi_debug_console_write(4, (unsigned long)"CAT\n", 0);

    char buffer[256];
    for (;;) {
        for (int i = 0; i < sizeof(buffer); i++) {
            buffer[i] = 0;
        }

        result = sbi_debug_console_read(sizeof(buffer) - 1, (unsigned long)&buffer[0], 0);
        sbi_debug_console_write(result.value, (unsigned long)&buffer[0], 0);
    }


    halt();
}

void panic(void) {
    __asm__ __volatile__("wfi");
    for (;;) { ; }
}

void halt(void) {
    sbi_system_reset(2, 0);
    __asm__ __volatile__("wfi");
    for (;;) { ; }
}
