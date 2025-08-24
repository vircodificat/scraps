#pragma once

#define BASE 0x00000010
#define DBCN 0x4442434E
#define SRST 0x53525354

struct sbiret {
    long error;
    long value;
};

struct sbiret sbi_call(long arg0, long arg1, long arg2, long arg3, long arg4, long arg5, long fid, long eid);

// BASE
struct sbiret sbi_get_spec_version(void);
struct sbiret sbi_get_impl_id(void);
struct sbiret sbi_get_impl_version(void);
struct sbiret sbi_probe_extension(long extension_id);
struct sbiret sbi_get_mvendorid(void);
struct sbiret sbi_get_marchid(void);
struct sbiret sbi_get_mimpid(void);

// DBCN
struct sbiret sbi_debug_console_write(unsigned long num_bytes, unsigned long base_addr_lo, unsigned long base_addr_hi);
struct sbiret sbi_debug_console_read(unsigned long num_bytes, unsigned long base_addr_lo, unsigned long base_addr_hi);
struct sbiret sbi_debug_console_write_byte(char byte);

// SRST
struct sbiret sbi_system_reset(short reset_type, short reset_reason);
