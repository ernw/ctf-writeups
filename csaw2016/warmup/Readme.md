# CSAW CTF 2016 warmup Writeup

coinslot was a pwn challenge for 50pts and the description of the challenge was

```
So you want to be a pwn-er huh? Well let's throw you an easy one ;)

nc pwn.chal.csaw.io 8000
```

Connecting to the server revealed the following:

```
$ nc pwn.chal.csaw.io 8000
-Warm Up-
WOW:0x40060d
>
```

At the end you can input some string. The binary that created this output was also provided. By reversing main function of the binary, we can see that the input is taken via a 'gets'.

```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char s;
  char v5;

  write(1, "-Warm Up-\n", 0xAuLL);
  write(1, "WOW:", 4uLL);
  sprintf(&s, "%p\n", easy);
  write(1, &s, 9uLL);
  write(1, ">", 1uLL);
  return gets(&v5, ">");
}
```

Moreover, there is an 'easy' function within the binary:

```
int easy()
{
  return system("cat flag.txt");
}
```

The address of this function is conveniently printed within the main function 

```
sprintf(&s, "%p\n", easy); 
```

and corresponds to the address 0x40060d.

By exploiting the gets-function, we can overwrite return addresses on the stack and gain control of $rip. Then we just jump to the easy-function and we are done. The exploit code is given in the warmup.py