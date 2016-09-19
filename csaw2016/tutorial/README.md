# CSAW CTF 2016 tutorial (200) Writeup

> Ok sport, now that you have had your Warmup, maybe you want to checkout the Tutorial.
>
>`nc pwn.chal.csaw.io 8002`

This time we have a pwning challenge which requires a ROP chain to exploit the vulnerability.

The program is very simple and shows a menu on startup:
```
-Tutorial-
1.Manual
2.Practice
3.Quit
```

The first menu entry prints the address where the `puts` function is currently loaded:
```
>1
Reference:0x7ffff7880860
```
The function looks approximately like this:
```c
void func1(int socket) {
    char bf[56];
    void* ref = dlsym(-1, "puts");
    write(socket, "Reference:", 10);
    sprintf(buf, "%p\n", ref);
    write(socket, buf, 15);
}
```

The second entry allows to send data to a function with a stack overflow:
```
>2
Time to test your exploit...
>asdasd
asdasd
�)������
```

The function contains a buffer which can contain 300 characters (actually 312 due to alignment).
as you can see in the pseudocode below, the `read` function reads 460 characters from the user.
Additionally it sends 324 characters back instead of the original 300.

```c
void func2(int socket) {
    char buffer[300];
    bzero(buffer, 300);
    write(socket, "Time to test your exploit...\n", 0x1d);
    write(socket, ">", 1);
    read(socket, buffer, 460);
    write(socket, buffer, 324);
}
```

This helps us as the function has a stack canary to protect against buffer overflows. As we can read
324 characters from the memory, we'll get the content of the stack canary and bypass the protection.

Based on these informations, I was able to reconstruct the address of the `libc` shared library and adjust my rop chain accordingly and bypass the stack protection:
[![asciicast](https://asciinema.org/a/bsnu9h035qeg5iffpcydhrru2.png)](https://asciinema.org/a/bsnu9h035qeg5iffpcydhrru2)

[1] [exploit script](exploit.py)
