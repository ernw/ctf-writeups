# CSAW CTF 2016 Broken Box Writeup

Broken Box was a crypto challenge for 300 pts

## Description

> I made a RSA signature box, but the hardware is too old that sometimes it returns me different answers... can you fix it for me?
>
> `e = 0x10001`
>
> `nc crypto.chal.csaw.io 8002`

Attached was a file named flag.enc, which holds the flag in encrypted form. When connecting to the service via netcat one is prompted for a number (0-9999) to sign. The service responds with the `signature` and the modulus `n`.

The overall task to get the flag was to somehow obtain the private key (we call it `d`) to decrypt the flag, which was supposedly encrypted with the known public key `e`.

## Solution

As the service description suggests, during the signing process a mistake happens and the service produces a wrong signature. One can filter wrong signatures by taking each to the power of `e` which should return the signed number. Also as the service returned the correct signature *most* of the time, one can easily find the correct one by looking at some signatures of the same number. In my attempt I always used 2 to be signed by the service, though it doesn't really matter, as long as the same number is taken for each signature.

At first we need to know what is going wrong when the service returns a wrong signature. It quickly became clear we are talking textbook RSA, so the signature is calculated with `m^d` (for `m=2` in our case). This can be found by checking a signature as just stated and due to the fact that the signature for 0 and 1 is always 0 and 1 respectively. So we don't have to worry about (erroneous) padding. But as I just said: the signature for 0 and 1 returned by the service was always 0 and 1. So that means the message `m` was not changed during the signing process, or else `0^d` and `1^d` would not yield 0 or 1. That means the exponent `d` is in someway changed. And according to the description we may hope that only one bit is flipped as the machine is "old".

Let's assume that we can represent the changed private key `d' = d + x`, where `x` is a power of 2, i.e. a number with only one 1 in its binary representation. This of course is not correct for all situations, as we use addition instead of xor, but if a bit in the former `d` is flipped from 0 to 1 this works as no overflow from the addition is caused. On the other hand if a bit is flipped from 1 to 0, we can represent the former `d = d' + x` without having trouble with the overflow.

When we put this together with a wrong signature `s` we received we have the following equations to test:
```
s = m^(d') = m^(d+x) = m^d * m^x
s = m^d = m^(d'+x) = m^(d') * m^x
```

So what we to is to simply bruteforce `m^x` and check the received signatures. Each wrong signature should yield a bit of the private key at a random position. As the modulus `n` is only 1024 bit long, `d` cannot be really longer. So we collect about 20k signatures and should have enough wrong ones to hit at least every bit at once. (This was just a guess from what I saw until then, but it worked.)

## Code

Let's put together some code:
```
i = 0
zeroBits = 0x0
oneBits = 0x0
job = log.progress("Testing sigs")
for sig in sigList:
    job.status("%6d" % (i))
    i += 1
    foundBit = False
    sigPart = 2

    #We check for more bits just to be safe
    for pos in range(0, 1050):

        # m^d = m^(d') * m^x
        newSig = (sig * sigPart) % n
        if newSig == correctSig:
            log.debug("Found 1 bit at position %d" % pos)
            oneBits |= 0x1 << pos
            break

        # m^(d') = m^d * m^x
        newSig = (correctSig * sigPart) % n
        if newSig == sig:
            log.debug("Found 0 bit at position %d" % pos)
            zeroBits |= 0x1 << pos
            break

        sigPart = (sigPart * sigPart) % n

    if not foundBit:
        log.debug("No bit found :(")

job.success("Done")
log.info("%x" % zeroBits)
log.info("%x" % oneBits)
```

## Result
Actually the above formula doesn't work as assumed and I didn't get a bit from each signature. Anyway, it even worked when I was able to check only for 1 bits in the private key. When doing this often enough there is a good chance that eventually all 1 bits are found and all other bits can be assumed as 0.

So here is the correct private key in hex:
```
bbb4a83f7736cab679ef7037818c8c2bd5aec69500040e4c84c45ddb13440e35dd32ea7a8c6b30d4540349f6bb78e01b08877a02e6c3f0e5cbbeffe6eee13da765c84345eb8acf42fe3437e5894d8cbff79af7e5c90596e0e3685ce89224b1199dc86e622a19ae51084168eb5307c93df5c856c9a4fede47a785f96499b68125
```

This yields the flag:
```
flag{br0k3n_h4rdw4r3_l34d5_70_b17_fl1pp1n6}
```

If you want to try it out yourself, you can find a list of faulty signatures in the *sigtest.list.7z* file.
