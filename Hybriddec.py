import custom_exceptions
import LSBSteg
import Hybridenc
import secrets
import random
import sys
import hashlib
import binascii
from termcolor import colored
from Crypto.Cipher import AES
from Crypto import Random


def decrypt(pk, ciphertext):
    d, n = pk
                                                                                 #5. m=c^d (mod n)
    m = [chr((char ** d) % n) for char in ciphertext]
    return m


def decryptAES(cipherAESd,cipherText):
    dec= cipherAESd.decrypt(cipherText).decode('utf-8')
    return dec


def DecryptHybrid():
#Decyrpting AES symm key
	decriptedKey=''.join(decrypt(Hybridenc.EncryptHybrid.rsa_pri,Hybridenc.EncryptHybrid.cipherkey))
	print(" ")
	print("Decrypting the AES Symmetric Key...\n\n")
	print("AES Symmetric Key:\n")
	print(colored(decriptedKey,'white'))
	print("\n\n")
	#2.	Uses this symmetric key to decrypt the message contained in the data encapsulation segment.
	decriptedKey=decriptedKey.encode('utf-8')
	cipherAESd = AES.new(decriptedKey, AES.MODE_GCM, nonce=Hybridenc.EncryptHybrid.nonce)
	decrypted=decryptAES(cipherAESd,Hybridenc.EncryptHybrid.ciphertext)
	print("Decrypting the message using the AES symmetric key.....\n\n")
	print("Decrypted message:")
	print(colored(decrypted,'white'))
	#print(decrypted)
	print(" ")

	message_digest2=decrypt(Hybridenc.EncryptHybrid.rsa_pri,Hybridenc.EncryptHybrid.DS)
	print('Decrypted digest from Digital signature\n')
	start, end = 0, 64
	res = ''.join([sub for sub in message_digest2])[start : end]
	print(colored(res,'white'))
	print(" ")

	print("Checking message Integrity...\n")

	sha_dec2 = decrypted.encode()
	result2 = hashlib.sha256(sha_dec2)
	hashval = result2.hexdigest()
	print('Hash value from Decrypted message:\n')
	print(colored(hashval,'white'))
	print(" ")
	if res == hashval:
		print(colored("\nThe message integrity is not violated!.",'red'))
	else:
		print("\nThe message integrity is violated.")

	print(" ")


if __name__ == "__main__":
    main()