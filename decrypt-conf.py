#!/usr/bin/python
import struct
from Crypto.Cipher import AES
import sys

KEY = "iwp2390x-e]57kx&#@*(ca,sfkf!eu+$"
IV = "fiw;opdd40382,*&"
OUT = '%s.txt'

def decrypt(settings):
    """Decrypt Optus Sagemcom F@st 3864 AES 56 CBC encrypted configuration file."""
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    with open(settings, 'rb') as infile:
        filebytes = infile.read()
    # first 4 bytes of the file is the length of the final clear text minus the padding
    cleartext_length = struct.unpack(">I", filebytes[:4])[0]

    with open(OUT % settings, 'wb') as outfile:
        outfile.write(cipher.decrypt(filebytes[4:]))
        outfile.truncate(cleartext_length-1)

if __name__ == '__main__':
    try:
        decrypt(sys.argv[1])
    except IndexError:
        print "usage: %s <settings file>" % sys.argv[0]
        sys.exit(2)
