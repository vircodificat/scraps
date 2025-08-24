#include "sbi.h"

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

// BASE
struct sbiret sbi_get_spec_version(void)    { return sbi_call(0, 0, 0, 0, 0, 0, 0, BASE); }
struct sbiret sbi_get_impl_id(void)         { return sbi_call(0, 0, 0, 0, 0, 0, 1, BASE); }
struct sbiret sbi_get_impl_version(void)    { return sbi_call(0, 0, 0, 0, 0, 0, 2, BASE); }
struct sbiret sbi_probe_extension(long eid) { return sbi_call(0, 0, 0, 0, 0, 0, 3, BASE); }
struct sbiret sbi_get_mvendorid(void)       { return sbi_call(0, 0, 0, 0, 0, 0, 4, BASE); }
struct sbiret sbi_get_marchid(void)         { return sbi_call(0, 0, 0, 0, 0, 0, 5, BASE); }
struct sbiret sbi_get_mimpid(void)          { return sbi_call(0, 0, 0, 0, 0, 0, 6, BASE); }

struct sbiret sbi_debug_console_write(
    unsigned long num_bytes,
    unsigned long base_addr_lo,
    unsigned long base_addr_hi
){
    return sbi_call(num_bytes, base_addr_lo, base_addr_hi, 0, 0, 0, 0, DBCN);
}

struct sbiret sbi_debug_console_read(
    unsigned long num_bytes,
    unsigned long base_addr_lo,
    unsigned long base_addr_hi
){
    return sbi_call(num_bytes, base_addr_lo, base_addr_hi, 0, 0, 0, 1, DBCN);
}

struct sbiret sbi_debug_console_write_byte(char byte) {
    return sbi_call(byte, 0, 0, 0, 0, 0, 2, DBCN);
}


struct sbiret sbi_system_reset(short reset_type, short reset_reason) {
    return sbi_call(reset_type, reset_reason, 0, 0, 0, 0, 2, DBCN);
}
