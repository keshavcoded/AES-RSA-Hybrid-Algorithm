import custom_exceptions
import LSBSteg
import secrets
import random
import sys
import hashlib
import binascii
from termcolor import colored
from Crypto.Cipher import AES
from Crypto import Random

def gcd(a, b):            #Euclid's algorithm         
        while b != 0:
            temp=a % b
            a=b
            b=temp
        return a

def multiplicativeInverse(a, b):  #Euclid's extended algorithm
        x = 0
        y = 1
        lx = 1
        ly = 0
        oa = a 
        ob = b  
        while b != 0:
            q = a // b
            (a, b) = (b, a % b)
            (x, lx) = ((lx - (q * x)), x)
            (y, ly) = ((ly - (q * y)), y)
        if lx < 0:
            lx += ob  
        if ly < 0:
            ly += oa  
        return lx


def isPrime(num):
    if (num < 2):
        return False      # 0, 1, and negative numbers are not prime

    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 
                 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 
                 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 
                 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 
                 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 
                 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 
                 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 
                 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 
                 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    
    if num in lowPrimes:
        return True
    
    for prime in lowPrimes:
        if (num % prime == 0): #refer
            return False
    
    return millerRabin(num)


def millerRabin(n, k = 7): #an algorithm which determines whether a given number is likely to be prime
    if n < 6:  
        return [False, False, True, True, False, True][n]
    elif n & 1 == 0:  
        return False
    else:
      s, d = 0, n - 1
      while d & 1 == 0:
         s, d = s + 1, d >> 1
      for a in random.sample(range(2, min(n - 2, sys.maxsize)), min(n - 4, k)):
         x = pow(a, d, n)  #pow(a, d) % n
         if x != 1 and x + 1 != n:
            for r in range(1, s):
               x = pow(x, 2, n)
               if x == 1:
                  return False 
               elif x == n - 1:
                  a = 0  
                  break 
            if a:
               return False  
      return True  


def generatePrime(keysize):
    while True:
        num = random.randrange(2**(keysize-1), 2**(keysize))  #random.randrange(start(opt),step(opt))
        if isPrime(num):
            return num

def KeyGeneration(size=8):
    #1. generate 2 large prime numbers
    p = generatePrime(size) 
    q = generatePrime(size)
    if not(isPrime(p) and isPrime(q)):
        raise ValueError('Both number must be prime')
    elif p==q:
        raise ValueError('p and q cannot be equal')

    #2.compute n=pq and pi=(p-1)(q-1)
    n = p * q
    pi = (p-1) * (q-1)

    #3.select random integer "e" (1<e<pi) such that gcd(e,pi)=1

    e = random.randrange(1, pi)
    g = gcd(e, pi)
    while g != 1:
        e = random.randrange(1, pi)
        g = gcd(e, pi)

    #4.Use Extended Euclid's Algorithm to compute another 
    #unique integer "d" (1<d<pi) such that e.d≡1(mod pi)
    
    d = multiplicativeInverse(e, pi)

    #5.Return public and private keys
    #Public key is (e, n) and private key is (d, n)
    return ((n, e), (d, n))

def encrypt(pk, pt):
    #1.obtain (n,e)
    n, e = pk
    #2.compute c=m^e(mod n)
    c = [(ord(char) ** e) % n for char in pt] #ord() equivalent ASCII value
    #print(c)
    return c

def encryptAES(cipherAES,plaintext):
    return cipherAES.encrypt(plaintext.encode("utf-8"))



def EncryptHybrid():
    print(" ")
    #To encrypt a message addressed to receiver, sender does the following
    #1. Obtains Receiver’s public key.
    print('Generating RSA Public and Private keys...')
    EncryptHybrid.rsa_pub,EncryptHybrid.rsa_pri=KeyGeneration()
    print(" ")
    print("*RSA Public and Private keys Successfully Generated*\n")

    #2. Generates a symmetric key for the data encapsulation scheme.
    print('Generating AES shared key...')
    key = secrets.token_hex(16) #Return a random text string, in hexadecimal. #or generating a random text string in hexadecimal containing nbytes random bytes
    #print key if needed
    KeyAES = key.encode('utf-8')  #utf-8 encoding scheme
    print(" ")
    print("*AES Secret key Successfully Generated*\n")
    print(' ')

    #3. Encrypts the message under the data encapsulation scheme,
    #   using the symmetric key just generated.

    plaintext = input("Enter the message: ")
    cipherAES = AES.new(KeyAES,AES.MODE_GCM)   #Galois/Counter Mode mode of operatiom
    EncryptHybrid.nonce = cipherAES.nonce
    print(" ")
    print("Encrypting the message with AES... ")
    EncryptHybrid.ciphertext = encryptAES(cipherAES,plaintext)
    print("AES cypher text: ")
    print(colored(EncryptHybrid.ciphertext, 'white'))
    print(" ")
    print("Ciphertext in hex:")
    Cipherhextext = binascii.hexlify(EncryptHybrid.ciphertext)
    print(colored(Cipherhextext,'white'))
    print(" ")


    #4. Encrypt the symmetric key under the key encapsulation scheme, using Alice’s public key.
    EncryptHybrid.cipherkey=encrypt(EncryptHybrid.rsa_pub,key)
    print("*Encrypting the AES symmetric key with RSA* ")
    print(" ")
    print("Encryted AES symmetric key")
    print(colored(EncryptHybrid.cipherkey,'white'))
    print(" ")

    #SHA256 Algorithm for finding message digest

    sha_enc = plaintext.encode()
    result = hashlib.sha256(sha_enc)
    message_digest = result.hexdigest()
    print('Message digest:\n')
    print(colored(message_digest,'white'))
    print(" ")

    #Digital signature
    EncryptHybrid.DS=encrypt(EncryptHybrid.rsa_pub,message_digest)
    print('Digital signature\n')
    print(colored(EncryptHybrid.DS,'white'))

if __name__ == "__main__":
    main()