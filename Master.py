import sys
import LSBSteg
import Hybridenc
import Hybriddec
import lsb_steganography_GUI
import lsb_steganography
import pyfiglet
from termcolor import colored
from pyfiglet import figlet_format
from pyfiglet import Figlet
from Crypto.Cipher import AES
from Crypto import Random


banner = pyfiglet.figlet_format(" HYBRID CRYPTOGRAPHIC SYSTEM")
print(colored(banner,'green'))

ch = 0
while ch!=4:
    ch = int(input(colored('What do you want to do?\n\n1.Encryption\n2.Stegnography\n3.Decryption\n4.Exit\n\nInput(1/2/3/4): ','blue')))
    if ch==1:
        Hybridenc.EncryptHybrid()
    elif ch==2:
        lsb_steganography.main()
    elif ch==3:
        Hybriddec.DecryptHybrid()