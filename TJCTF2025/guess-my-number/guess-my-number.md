# Information
- **CTF:** *TJCTF*
- **Challenge name:** *guess-my-number*
- **Challenge description:** *You only get ten tries to guess the number correctly, but I tell you if your guess is too high or too low*
- **Category:** *misc*
- **Date:** *June 2025*
# Approach
We are provided an address that we can connect to using netcat. From the challenge description as well as the prompts from the server when we connect, we can easily deduce that it is testing us on using the binary search algorithm to find out the secret number.

All we have to do to obtain the flag is to perform binary search and 'guess' the number, and upon the correct 'guess', we are provided with the flag.

You can read more about [binary search here](https://en.wikipedia.org/wiki/Binary_search).
# Flag
```tjctf{g0od_j0b_u_gu33sed_correct_998}```
# Tags
- TJCTF
- Beginner
---
*Written on 09-06-2025*

