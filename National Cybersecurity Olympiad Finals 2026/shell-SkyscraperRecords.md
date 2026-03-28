# Shell - SkyscraperRecords

## Solution TL;DR
Decrypt TLS packets in `.pcap` file with provided `SSLKEYLOGFILE` using Wireshark and analyse the packets to determine commands to send to the remote server to retrieve the flag.

## Information
- **CTF:** National Cybersecurity Olympiad (Finals) 2026 - Singapore
- **Challenge name:** *Shell*
- **Challenge series:** *SkyscraperRecords*
- **Date:** *March 2026*

## Approach
We are provided with a PCAP file, an SSL keylog file and a remote server to connect to.  

Opening the PCAP file in Wireshark, we see multiple TLS and TCP packets. When trying to follow the TCP stream, we see gibberish. The observed gibberish and the presence of an SSL keylog file strongly suggest that we need to decrypt the packets.

Following [this guide](https://unit42.paloaltonetworks.com/wireshark-tutorial-decrypting-https-traffic/), we can load the SSL keylog file and perform the decryption then follow the readable TLS stream:
```
[AUTH] input password > 
robotsweepsweepsweep

[ENSIOH] > 
show_cmds

[?] cmds:
show_cmds - show this message
show_secret - show secret
[?] unrecognized command!
[ENSIOH] > 
``` 

Connecting to the remote server via `nc`, we see that we are presented with a similar prompt as captured in the log. After logging in with the password `robotsweepsweepsweep`, we can simply use the command `show_secret` to print our flag.

## Flag
```NCO26{dont_y0u_l0v3_th3_1nt3rn3t_0f_th1ngs}```

## Tags
- NCO 2026
- Forensics
- TLS decryption

## References
1. https://unit42.paloaltonetworks.com/wireshark-tutorial-decrypting-https-traffic/

---
*Written on 28-03-2026 by gr*
