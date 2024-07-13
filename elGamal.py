import random
from math import isqrt

class Gamal:
    
    def __init__(self):
        pass

    def find_random_prime(self):
        min_val = 299
        max_val = 999
        while True:
            i = random.randint(min_val, max_val)
            if self.is_prime(i):
                return i

    def is_prime(self, num):
        if num <= 1:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, isqrt(num) + 1, 2):
            if num % i == 0:
                return False
        return True

    def mpmod(self, base, exponent, modulus):
        if base < 1 or exponent < 0 or modulus < 1:
            return "invalid"
        result = 1
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            base = (base * base) % modulus
            exponent = exponent // 2
        return result

    def find_primitives(self, the_num):
        o = 1
        roots = []
        
        for r in range(2, the_num):
            k = pow(r, o) % the_num
            while k > 1:
                o += 1
                k *= r
                k %= the_num
            if o == (the_num - 1):
                roots.append(r)
            o = 1

        return roots

    def encrypt(self, q, a, ya, message):
        ciphers = {}
        every_separate = ""

        k1 = random.randint(2, q - 1)
        k2 = self.mpmod(ya, k1, q)
        c1 = self.mpmod(a, k1, q)
        c2 = ""

        for char in message:
            current_char = ord(char)
            current_c2 = (k2 * current_char) % q
            c2 += str(current_c2)
            every_separate += str(len(str(current_c2)))

        ciphers[0] = c1
        ciphers[1] = c2
        ciphers[2] = every_separate
        return ciphers

    def decrypt(self, c1, c2, xa, q, every_separate):
        m = ""
        k2 = self.mpmod(c1, xa, q)
        k2_inverse = self.mod_inverse(k2, q)

        c2 = str(c2)
        index = 0
        for length in every_separate:
            length = int(length)
            current_segment = c2[index:index + length]
            index += length
            m += self.get_the_current_char(current_segment, k2_inverse, q)
        return m

    def get_the_current_char(self, segment, k2_inverse, q):
        current = int(segment)
        return chr((k2_inverse * current) % q)

    def mod_inverse(self, a, m):
        for x in range(1, m):
            if ((a % m) * (x % m)) % m == 1:
                return x

# Example usage
gamal = Gamal()
q = gamal.find_random_prime()
primitives = gamal.find_primitives(q)
a = primitives[0] if primitives else None
xa = random.randint(2, q - 2)
ya = gamal.mpmod(a, xa, q)

message = "Hello"
ciphertext = gamal.encrypt(q, a, ya, message)
print("Ciphertext:", ciphertext)

decrypted_message = gamal.decrypt(ciphertext[0], ciphertext[1], xa, q, ciphertext[2])
print("Decrypted Message:", decrypted_message)
