# Information
- **CTF:** TJCTF
- **Challenge name:** *deep-layers*
- **Challenge description:** *Not everything ends where it seems to...*
- **Category:** *forensics*
- **Date:** *June 2025*
# Approach
We are provided with a PNG file (`chall.png`), and upon downloading and opening the image, it doesn't seem to display any content.

Our next step would be to gather more info on this file. Using `exiftool`, we are able to analyse the metadata of the image. We obtain the following output:
```
└─$ exiftool chall.png
ExifTool Version Number         : 13.10
File Name                       : chall.png
Directory                       : .
File Size                       : 370 bytes
File Modification Date/Time     : 2025:06:06 12:57:43+08:00
File Access Date/Time           : 2025:06:07 15:10:48+08:00
File Inode Change Date/Time     : 2025:06:07 15:10:45+08:00
File Permissions                : -rw-r--r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 1
Image Height                    : 1
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Password                        : cDBseWdsMHRwM3NzdzByZA==
Warning                         : [minor] Trailer data after PNG IEND chunk
Image Size                      : 1x1
Megapixels                      : 0.000001
```

Hmm, interesting. There are two pieces of information here that caught my attention:
- The password field with the following data (this data is base 64 encoded): `cDBseWdsMHRwM3NzdzByZA==`
- The warning field which tells us there is trailing data present after the supposed end of the PNG file

For the data in the password field, decoding it yields the following string: `p0lygl0tp3ssw0rd`. This string is presumably a password for something (*some foreshadowing here 😉*).

To find out if there is extractable data present in the file, we can use the `binwalk` tool:
```
└─$ binwalk chall.png

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 1 x 1, 8-bit/color RGBA, non-interlaced
90            0x5A            Zlib compressed data, default compression
119           0x77            Zip archive data, encrypted at least v1.0 to extract, compressed size: 67, uncompressed size: 55, name: secret.gz
348           0x15C           End of Zip archive, footer length: 22
```

There is indeed a zip file present that we can extract! We can extract the zip file using the command `binwalk -e chall.png` and then attempt to unzip the file.

Guess what, we are indeed prompted for a password! Supplying `p0lygl0tp3ssw0rd`, we are indeed able to unzip the file and extract a file that when printed to the console, provides us with the flag.
# Flag
```tjctf{p0lygl0t_r3bb1t_h0l3}```
# Tags
- TJCTF
- Forensics
- Binwalk
- Hidden data
---
*Written on 09-06-2025*

