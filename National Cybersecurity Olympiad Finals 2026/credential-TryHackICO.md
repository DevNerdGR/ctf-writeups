# Credential - TryHackICO

## Solution TL;DR
Cracking and retrieving the credentials stored by Windows Credential Manager allows us to obtain the flag. The cracking process involves first cracking the user account's password by bruteforcing the associated NTLM hash, then using the password to unlock the `dpapi` master key used to decrypting the credentials.

[Mimikatz](https://github.com/ParrotSec/mimikatz), [hashcat](https://hashcat.net/hashcat/) and [DIANA](https://github.com/tijldeneut/diana) were rather helpful. Do consider checking them out if you are doing a similar challenge where you need to recover credentials from a Windows machine disk image. 

## Information
- **CTF:** National Cybersecurity Olympiad (Finals) 2026 - Singapore
- **Challenge name:** *Credential*
- **Challenge series:** *TryHackICO*
- **Date:** *March 2026*

## Approach
### Introduction
We are presented with a disk image. When opened with [autopsy](https://www.autopsy.com/), we can tell that we are dealing with a Windows disk image. This particular challenge description hinted at the "Credential Manager" containing some *interesting* information. Some simple searching will reveal that we are probably looking at extracting credentials stored by the Windows Credential Manager. The Windows Credential Manager is essentially a tool that *securely* stores and manages credentials, allowing for automatic login to services.

### About Windows Credential Manager
Credentials are mainly stored encrypted and can be found in `C:\Users\<user>\AppData\Local\Microsoft\Credentials` and `C:\Users\<user>\AppData\Roaming\Microsoft\Credentials`. 

Windows Credential Manager uses the [Data Protection API (`dpapi`)](https://en.wikipedia.org/wiki/Data_Protection_API) to secure the credential files. At a high level, `dpapi` is an API that secures data, in this case, using the user's password (for a deeper dive into `dpapi`, check out the paper by [Burztein et. al.](https://www.usenix.org/legacy/event/woot10/tech/full_papers/Burzstein.pdf)). Internally, `dpapi` generates master key files which is what is actually used to secure the credential files.

Hence, to crack the credential files, our next step is naturally to obtain the user's password

### Retrieving the flag
#### Cracking Windows user password
Fortunately, this is a relatively well known task that [Mimikatz](https://github.com/ParrotSec/mimikatz) and [hashcat](https://hashcat.net/hashcat/) can help us with. 

We first need to export the `SAM` and `SYSTEM` registry keys. They can be located at `C:\Windows\System32\config\SAM` and `C:\Windows\System32\config\SYSTEM`. Simply export them from autopsy.

Now, enter `lsadump::sam /system:<path/to/exported/SYSTEM>
/SAM:<path/to/exported/SAM>` into the Mimikatz console.
```
mimikatz # lsadump::sam /system:<path/to/exported/SYSTEM> /sam:<path/to/exported/SAM>
Domain : NCO-TRYHACKICO
SysKey : 5e19d07f4a28f488ef4f774a9b706647
Local SID : S-1-5-21-1337044915-1330413738-4044976850

SAMKey : 73a6c2aec44b8a1f05cb6058f517cfb6

...

RID  : 000003e8 (1000)
User : red
  Hash NTLM: e550853afc9a68106d73fd6680b25604 <<< hash of user's password

...
``` 

The NTLM hash stores the hashed user password and is what we need to crack. We can use hashcat to help us with the bruteforce cracking process. After saving the obtained hash into a file, the following command bruteforces the password using the `rockyou.txt` wordlist:
```bash
$ hashcat -m 1000 -a 0 <path/to/hash> /usr/share/wordlists/rockyou.txt
```
Hashcat successfully cracks the hash, informing us that the password is `mychemicalromance`.

#### Retrieving the flag
Diana is a script library that provides scripts for forensic work with various aspects of credential management in Windows. While Diana does provide scripts that allow us to decrypt and retrieve the master keys, we can also directly decrypt the credential files using the `diana-creddec.py`.

Before we use the script, we should retrieve the following files from our disk image:
- Master keys directory `C:\Users\<user>\AppData\Roaming\Microsoft\Protect\`
- Credential files `C:\Users\<user>\AppData\Local\Microsoft\Credentials` and `C:\Users\<user>\AppData\Roaming\Microsoft\Credentials`

We can now use the `diana-creddec.py` script to decrypt our credential files
```
$ diana-creddec.py --masterkey=<master/key/directory> --password=mychemicalromance <directory/of/credential/files>
[+] Detected SID: S-1-5-21-1337044915-1330413738-4044976850-1000
-------- Working on file 952B742593C21B907C5E6A3309922978 --------
[+] Last Update : 2026-03-11 00:47:49
[+] Main Data
    Domain   : LegacyGeneric:target=flag.nco
    Data1    :
    Data2    :
    Data3    :
    Username : red
    Password : NCO26{on_and_on_and_on_and_on}
######################################################################
-------- Working on file DFBE70A7E5CC19A398EBF1B96859CE5D --------
[+] Last Update : 2026-03-11 01:00:23
[+] Main Data
    Domain   : WindowsLive:target=virtualapp/didlogical
    Data1    :
    Data2    : PersistedCredential
    Data3    :
    Username : 02czbzqfzjkkqqrv
    Password :
[+] Found another DPAPI blob, decrypting now
[-] MasterKey with GUID 126a6dd7-d1be-46ee-9c4d-d9a84c5e5e7e not found for blob.
     Writing to 126a6dd7-d1be-46ee-9c4d-d9a84c5e5e7e.blob for manual decryption later
######################################################################

```
And there we have our flag!

## Flag
```NCO26{on_and_on_and_on_and_on}```

## Tags
- NCO 2026
- Forens
- Windows disk image
- Credentials extraction
- Windows Credential Manager
- Data protection API (`dpapi`)

## References
1. https://attack.mitre.org/techniques/T1555/004/
2. https://www.nitttrchd.ac.in/imee/Labmanuals/Password%20Cracking%20of%20Windows%20Operating%20System.pdf
3. https://github.com/tijldeneut/diana
4. https://www.thehacker.recipes/ad/movement/credentials/dumping/windows-credential-manager
5. https://en.wikipedia.org/wiki/Data_Protection_API
6. https://www.synacktiv.com/publications/windows-secrets-extraction-a-summary
7. https://www.usenix.org/legacy/event/woot10/tech/full_papers/Burzstein.pdf

## Appendix - an extension into `vault`
The method of using `dpapi` to secure credentials presented here is an older (but still used) method of securing credentials. A newer method (vault) makes use of `dpapi` to instead protect a key (stored in `Policy.vpol`) that is used to protect credential files (`*.vcrd`).
```
user's password ---protects---> master keys ---protects---> Policy.vpol ---protects---> *.vcrd
```
It is worth noting that Diana is also able to work with vault. 

This actually caused me some confusion, and it was only when writing this writeup did I realise I mixed them up.

---
*This was honestly my favourite solve and I had a lot of fun. I'm also really proud because I blooded it and it only had a total of 2 solves :).*

*Written on 28-03-2026 by gr*
