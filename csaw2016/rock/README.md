# CSAW CTF 2016 The Rock (100) Writeup

> Never forget the people's champ.

This challenge was about reversing a amd64 linux binary. I you look at the main
function with radare2, you'll notice that it seems to be a program written in c++
(due to the usage of `std::cin`, `std::cout` and `std::string`).

If you manually translate the disassembly into a c++ source code, it should roughly
look like:


```c++
int main(int argc, char** argv) {
    std::string input;
    struct S1 target;

    std::cin >> input;

    std::cout << "-------------------------------------------" << std::endl;
    std::cout << "Quote from people's champ" << std::endl;
    std::cout << "-------------------------------------------" << std::endl;
    std::cout << "*My goal was never to be the loudest or the craziest. It was to be the most entertaining." << std::endl;
    std::cout << "*Wrestling was like stand-up comedy for me." << std::endl;
    std::cout << "*I like to use the hard times in the past to motivate me today." << std::endl;
    std::cout << "-------------------------------------------" << std::endl;

    fcn_004015dc(&target, &input);
    std::cout << "Checking...." << std::endl;
    {
        std::string foo(input);
        std::string bar, baz, bla;
        fcn_0040114c(&bar, &foo);
        fcn_004010bf(&baz, &bar);
        fcn_00400ffd(&bla, &baz);
    }
    fcn_004016ba(&target);
    if(!fcn_004017e6(&target)) {
        std::cout << "/////////////////////////////////" << std::endl;
        std::cout << "Do not be angry. Happy Hacking :)" << std::endl;
        std::cout << "/////////////////////////////////" << std::endl;

        std::string output;
        fcn_004018d6(&output, &target);
        std::cout << "Flag{" << output << "}" << std::endl;
    }
    fcn_00401920(&target);

    return 0;
}
```

The given input seems to be processed in the functions `fcn_004015dc`, `fcn_004016ba`, `fcn_004017e6` and `fcn_004018d6`.
The functions `fcn_0040114c`, `fcn_004010bf` and `fcn_00400ffd` operate only on a copy of the input and the result isn't used
afterwards, therefore it might only be for obfuscation.

The first function (`fcn_004015dc`) shows that the first parameter is actually a class (and the function possibly a constructor).
The function sets one field to zero, stores two copies of our input and a third one with the string `FLAG23456912365453475897834567`
prepended.

```c++
struct S1 {
    void *vtable;
    int32_t x;
    std::string* input;
    std::string& input2;
    std::string& foo;
};
fcn_004015dc(struct S1* a, std::string& b) {
    fcn_004015c6(a);

    a->vtable = 0x401bf0;
    a->x = 0;
    a->input = std::string(b);
    a->input2 = std::string(b);
    a->foo = "FLAG23456912365453475897834567" + std::string(b);
}
```

The second function called checks if the input string is exactly 30 characters long. If this is true, it xors each character with
`0x50` and adds `20` to them. After that, it xors them with `16` and adds `9`.

```c++
fcn_004016ba(struct S1* a) {
    if(a->input.length() != 30) {
        std::cout << "Too short or too long" << std::endl;
        exit(-1);
    }

    for(int i = 0; i < ; i++) {
        a->input[i] = (a->input[i] ^ 0x50) + 20;
    }

    for(int j = 0; j < ; j++) {
        a->input[i] = (a->input[i] ^ 0x10) + 9;
    }
}
```

The third function has to return zero to continue to the output of the flag. As you can see, it compares the characters of the `foo`
field of the class (the string `FLAG...`). Only if all characters are equal, we can proceed to the flag output.
```c++
fcn_004017e6(struct S1* a) {
    for(int i = 0; i < a->input.length(); i++) {
        if(a->input[i] != a->foo[i]) {
            std::cout << "You did not pass " << i << std::endl;
            a->x = 1;         
            break;
        }
        std::cout << "Pass " << i << std::endl;
    }
    return a->x;
}
```

The function inside the if body simply copies the `input2` field to a new value (this field contains a unmodified copy of our input).
```c++
fcn_004018d6(std::string& a, struct S1* b) {
    a = b->input2;
}
```

This means that our input is actually the flag if it passes the `fcn_004017e6` check. We know that the input is transformed in the
function `fcn_004016ba` and afterwards compared to the string `FLAG23456912365453475897834567`. So all we have to do is to reverse the transformation. I've done this with python(3):
```python
>>> bytes([(((a - 9) ^ 16) - 20) ^ 0x50 for a in b"FLAG23456912365453475897834567"])
b'IoDJuvwxy\\tuvyxwxvwzx{\\z{vwxyz'
```
Our flag is `Flag{IoDJuvwxy\tuvyxwxvwzx{\z{vwxyz}`
