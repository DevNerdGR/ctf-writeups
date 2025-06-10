# Information
- **CTF:** *TJCTF*
- **Challenge name:** *front-door*
- **Challenge description:** *The admin of this site is a very special person. He's so special, everyone strives to become him.*
- **Category:** *web*
- **Date:** *June 2025*
# Approach
For this challenge, we are provided with only a URL to the target website.

Upon visiting the website, we are greeted with a very bare but functional homepage containing 2 buttons - one that leads us to the products page, and another that leads us to the account creation page.

If we browse over to the products page and scroll to the bottom, we uncover this very interesting chunk of text:
![hash algorithm](hashAlgo.png)

Wow! I see jwt! This must be a challenge relating to JSON Web Tokens (JWTs for short). We can then proceed to create an account and then inspect the cookies stored by this website. Indeed, we find a JWT (note: **never** reveal your JWTs, they are credentials! I only chose to expose mine here as this does not contain real life sensitive data.): `eyJhbGciOiAiQURNSU5IQVNIIiwgInR5cCI6ICJKV1QifQ.eyJ1c2VybmFtZSI6ICJhYWEiLCAicGFzc3dvcmQiOiAiYWFhIiwgImFkbWluIjogImZhbHNlIn0.JZOAYHBBBBNBDDQABXBFJOABZBLBBSOBVLBWVBQRSJJBOJYXDQZBEIRQBSOOFFWB`

Attempting to decode this in a JWT decoder website, we are met with the following:
![decoded jwt](jwt.png)

As we can see, this JWT seems to be using a custom hashing algorithm to validate the integrity and authenticity of the token. We also find that under the payload section, there is a field that specifies whether a user has admin privileges or not. Our challenge now would be to generate a valid JWT token that has the `admin` field set as `true`.

I initially went directly to try to reverse and figure out how the 'revolutionary new hashing algorithm' works. However, after a while, I noticed that a key was required. Conventional JWTs (using common algorithms) are usually signed by the server using a private key. In this case, we might be led to assume that this algorithm does the same. This thus makes it very challenging to reverse algorithm for us to generate valid signatures.

I then tried to create a few different accounts to see how the signature changed with different username/password combinations, hoping to spot a pattern that I could then exploit.

Instead, I observed the following: **all JWTs, regardless of content, had the same signature!**
```python
token = "eyJhbGciOiAiQURNSU5IQVNIIiwgInR5cCI6ICJKV1QifQ.eyJ1c2VybmFtZSI6ICIxIiwgInBhc3N3b3JkIjogInF3ZXF3ZSIsICJhZG1pbiI6ICJmYWxzZSJ9.JZOAYHBBBBNBDDQABXBFJOABZBLBBSOBVLBWVBQRSJJBOJYXDQZBEIRQBSOOFFWB"

token2 = "eyJhbGciOiAiQURNSU5IQVNIIiwgInR5cCI6ICJKV1QifQ.eyJ1c2VybmFtZSI6ICJhIiwgInBhc3N3b3JkIjogImEiLCAiYWRtaW4iOiAiZmFsc2UifQ.JZOAYHBBBBNBDDQABXBFJOABZBLBBSOBVLBWVBQRSJJBOJYXDQZBEIRQBSOOFFWB"

token3 = "eyJhbGciOiAiQURNSU5IQVNIIiwgInR5cCI6ICJKV1QifQ.eyJ1c2VybmFtZSI6ICIxMjQxMjEyIiwgInBhc3N3b3JkIjogImhlaGVoZWhlaCIsICJhZG1pbiI6ICJmYWxzZSJ9.JZOAYHBBBBNBDDQABXBFJOABZBLBBSOBVLBWVBQRSJJBOJYXDQZBEIRQBSOOFFWB"
```

I then generated my own admin token, by simply decoding the payload section (note: data in JWTs are base64 encoded), changing the `admin` field to `true`, then encoding the payload again, yielding the following JWT:
```python
tokenModded = "eyJhbGciOiAiQURNSU5IQVNIIiwgInR5cCI6ICJKV1QifQ.eyJ1c2VybmFtZSI6ICIxIiwgInBhc3N3b3JkIjogInF3ZXF3ZSIsICJhZG1pbiI6ICJ0cnVlIn0=.JZOAYHBBBBNBDDQABXBFJOABZBLBBSOBVLBWVBQRSJJBOJYXDQZBEIRQBSOOFFWB" #Correct token
```

Replacing the original JWT in the browser with this modded JWT, we are granted admin access! On navigating to the homepage, we are met with a new button that brings us to the todo page. On the todo page, we are presented with the following and we are told to decrypt the code.
```
[108, 67, 82, 10, 77, 70, 67, 94, 73, 66, 79, 89]  
[107, 78, 92, 79, 88, 94, 67, 89, 79, 10, 73, 69, 71, 90, 75, 68, 83]  
[105, 88, 79, 75, 94, 79, 10, 8, 72, 95, 89, 67, 68, 79, 89, 89, 117, 89, 79, 73, 88, 79, 94, 89, 8, 10, 90, 75, 77, 79, 10, 7, 7, 10, 71, 75, 78, 79, 10, 67, 94, 10, 72, 95, 94, 10, 68, 69, 10, 72, 95, 94, 94, 69, 68, 10, 94, 69, 10, 75, 73, 73, 79, 89, 89, 10, 83, 79, 94]  
[126, 75, 65, 79, 10, 69, 92, 79, 88, 10, 94, 66, 79, 10, 93, 69, 88, 70, 78, 10, 7, 7, 10, 75, 70, 71, 69, 89, 94, 10, 78, 69, 68, 79]
```

Instead of trying directly to brute force/decode this encrypted message, if we attempt to gather more information and navigate to the `robots.txt` file, we find the following content present:
```
User-agent: * 
Disallow: 

# Gonna jot the encryption scheme I use down for later -The Incredible Admin
#
# def encrypt(inp):
#   enc = [13]
#   for i in range(len(inp)):
#     enc.append(ord(inp[i]) ^ 42)
#   return enc[1:]
```

Which if we read and understand the code, it is simply performing XOR encryption using the value 42 as a key! Applying this new information to perform decryption, we obtain the following strings:
```
Fix glitches
Advertise company
Create "business_secrets" page -- made it but no button to access yet
Take over the world -- almost done
```

If we visit the `business_secrets` page, we are rewarded with the flag.
# Flag
```tjctf{buy_h1gh_s3l1_l0w}```
# Tags
- TJCTF
- Web
- JWT
- XOR
---
*Written on 09-06-2025*

