# Notes - Base26

## Solution TL;DR
Crack the [linear congruential generator (LCG)](https://en.wikipedia.org/wiki/Linear_congruential_generator) pseudo RNG algorithm to recover the seed values and obtain the flag.

## Information
- **CTF:** National Cybersecurity Olympiad (Finals) 2026 - Singapore
- **Challenge name:** *Notes*
- **Challenge series:** *Base26*
- **Date:** *March 2026*

## Approach
Inspecting the code of the provided `server.py` file (code attached in appendix), we are able to see clearly that the goal is to somehow crack the pseudo RNG algorithm and retrieve the first RNG value. The algorithm used is the [linear congruential generator (LCG)](https://en.wikipedia.org/wiki/Linear_congruential_generator) algorithm.

Following [this guide](https://github.com/jiegec/ctf-writeups/blob/master/docs/misc/lcg.md), we can adapt the script for our use:
```python
# recover LCG
# given an array of x_i
# x_{i+1} = (ax_i + b) \bmod p

from Crypto.Util.number import *
import math

# 4 passwords obtained from the remote server (i.e. 4 outputs of the LCG RNG)
x = [42072641968992117988467423942178957131770671527348361553495530957525213974214, 40438847064617280208479057670270738077408347113948958881887395499898022685820, 34659606486582396725681889662701594917758321429147236792689645329573849470020, 4584145049008354001838973233700234447477732237332056519542616719169079383545]

# recover p
# compute y_i = x_{i+1} - x_i
y = []
for i in range(len(x) - 1):
    y.append(x[i + 1] - x[i])

# compute z_i = y_{i+2}y_i - y_{i+1}^2
z = []
for i in range(len(y) - 2):
    z.append(y[i + 2] * y[i] - y[i + 1] ** 2)

# compute gcd, we found p
p = 2**255-19 # Obtained from provided server.py
print("p is found")

# compute a from y_iy_{i-1}^{-1} \bmod p
a = (y[1] * pow(y[0], -1, p)) % p
print("a is found")

# compute b from (x_{i+1} - ax_i) \bmod p
b = (x[1] - a * x[0]) % p
print("b is found")

# find initial state x_0 = (x_1 - b) * a^{-1} \bmod p
x0 = (x[0] - b) * pow(a, -1, p) % p
print("initial state is found")

print(f"{p=} {a=} {b=} {x0=}")
```

We can now simply read the stored flag using `x0` as the password.

## Flag
```NCO26{LCG_st4nd5_for_Let5_Crack_th15_Gen3rator}```

## Tags
- NCO 2026
- Crypto
- Rev
- Linear congruential generator (LCG)

## References
1. https://en.wikipedia.org/wiki/Linear_congruential_generator
2. https://github.com/jiegec/ctf-writeups/blob/master/docs/misc/lcg.md

## Appendix - `server.py`
```python
import os
import secrets

def lcg(a, b, p, x):
    while True:
        x = (a * x + b) % p
        yield x

p = 2**255-19
x, a, b = [secrets.randbelow(p) for _ in range(3)]

flag = os.environ.get('FLAG','NCO26{test_flag}')
notes = [{'password':x,'content':flag}]

rng = lcg(a,b,p,x)

banner = '''
              _                    ____   __               
  _____ _____| |__   __ _ ___  ___|___ \ / /_  _____ _____ 
 |_____|_____| '_ \ / _` / __|/ _ \ __) | '_ \|_____|_____|
 |_____|_____| |_) | (_| \__ \  __// __/| (_) |_____|_____|
             |_.__/ \__,_|___/\___|_____|\___/             

Welcome to base26 note-taking platform!'''

print(banner)
while True:
    print('''Choose your option:
1. Take note
2. Read note
3. Exit''')
    choice = int(input())
    match choice:
        case 1:
            content = input('Enter the note content: ')
            password = next(rng)
            notes.append({'password':password,'content':content})
            print('Your note is at index',len(notes)-1)
            print('Your note password is:',password)
        case 2:
            idx = int(input('Enter the note index you wish to read: '))
            password = int(input('Enter the note password: '))
            if notes[idx]['password'] == password:
                print(notes[idx]['content'])
            else:
                print('Wrong password')
        case _:
            break
    print()

``` 

---
*Written on 28-03-2026 by gr*