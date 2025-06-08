# Information
- **CTF:** *Grey Cat The Flag 2025 Qualifiers*
- **Challenge name:** *Tung Tung Tung Sahur*
- **Challenge description:** 
>	*New to the world of brainrot? Not sure what names to pick from? We've got you covered with a list of our faves:*
>		*- Tralalero Tralala*  
>		*- Chef Crabracadabra*
>		*- Boneca Ambalabu*
>		*- Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur*
- **Category:** *EZPZ*
- **Date:** *June 2025*
# Approach
We are provided with two files: 
- `output.txt`: Contains a bunch of tungs, a sahur and values of `e`, `N` and `C`, presumably the output of `tung_tung_tung_sahur.py`. The presence of `e`, `N` and `C` reminded me of RSA
- `tung_tung_tung_sahur.py`: Upon inspection, it is evident that this script encrypted the password and generated `output.txt`
Our task now is to decrypt the given ciphertext `C`!

Further inspection of the python script leads us to the conclusion that we just need to 'reverse' each step of the code (and no bruteforcing is required).

If we attempt to 'reverse' each step, we might end up with the following code snippet:
```python
#...
C += N
for i in range(164): 
	C /= 2
m = C ** (1 / 3) 
m = long_to_bytes(int(m)).decode()
#...
```

At this point, if we attempt to simply print out the value of `m`, we will notice that only the first few characters make sense. This issue is caused by the fact that in the code snippet above, we used floating point operations.

Floating point operations introduce precision errors, and in this case of cryptography where every single byte matters, we cannot afford to lose precision by using floating point operations!

Hence, the corrected snippet should be as follows:
```python
#...
C += N
for i in range(164): 
	C //= 2
m = iroot3(C) 
m = long_to_bytes(int(m)).decode()
#...
```

Where we have replaced the division operation with the integer division operation and the cube root operation with a integer cube root operation.

The integer cube root operation was a function written by us - it uses binary search to obtain the cube root of a given cube number.
```python
def iroot3(n):
    lo = 0
    hi = n
    while lo <= hi:
        mid = lo + ((hi - lo) // 2)
        if n > mid ** 3:
            lo = mid
        elif n < mid ** 3:
            hi = mid
        else:
            return mid
```

With the precision issue resolved, we can go ahead and decode the bytes to obtain the flag!
# Flag
```grey{tUn9_t00nG_t0ONg_x7_th3n_s4hUr}```
# Tags
- Grey Cat The Flag 2025
- Crypto
- Beginner
---
*Written on 08-06-2025*

![[tungtungtungsahur.png]]
