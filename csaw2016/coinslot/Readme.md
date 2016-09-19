# CSAW CTF 2016 coinslot Writeup

coinslot was a challenge for 25pts and the description of the challenge was

```
nc misc.chal.csaw.io 8000
```

Connecting to the server revealed the coinslot game. The coinslot game goes as follows: You are given a certain amount of dollars. Then you have to represent this amount with the least possible number of coins and dollar bills. Basically, the game asks you how much of each coin or bill you would like to provide. Here is an example:

```
$ nc misc.chal.csaw.io 8000
$0.08
$10,000 bills: 0
$5,000 bills: 0
$1,000 bills: 0
$500 bills: 0
$100 bills: 0
$50 bills: 0
$20 bills: 0
$10 bills: 0
$5 bills: 0
$1 bills: 0
half-dollars (50c): 0 
quarters (25c): 0
dimes (10c): 0
nickels (5c): 1
pennies (1c): 3
correct!
$0.09
$10,000 bills: [and so on...]
```

Therefore, we just have to write a script that solves this game until, finally, the flag is dropped. I have attached the script I created as "coinslot.py".

The program is very simple. Basically, it consists of a (float sensitive) modulo function which is used to solve the indiviual rounds. When the script is running, the amount thar is present will slowly increase. After a certain number of games (maybe around 1000) the flag was presented. 