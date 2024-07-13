import random

class Gamal:
    
    def __init__(self):
        pass

    def is_prime(self, n):
        """  Miller-Rabin test """
        if n == 2 or n == 3:
            return True
        if n <= 1 or n % 2 == 0:
            return False

        # Write n-1 as d * 2^r
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        # Witness loop
        def witness(a, d, n):
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                return False
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    return False
            return True

        # Perform Miller-Rabin test with 10 iterations
        for _ in range(10):
            a = random.randint(2, n - 2)
            if witness(a, d, n):
                return False
        return True

    def find_primitive_root(self, p):
        """ Find a primitive root modulo p """
        if p == 2:
            return 1
        phi = p - 1
        prime_factors = self.get_prime_factors(phi)
        for g in range(2, p):
            if all(pow(g, phi // pf, p) != 1 for pf in prime_factors):
                return g
        return None

    def get_prime_factors(self, n):
        """ Get the prime factors of a number """
        factors = set()
        while n % 2 == 0:
            factors.add(2)
            n //= 2
        for i in range(3, int(n**0.5) + 1, 2):
            while n % i == 0:
                factors.add(i)
                n //= i
        if n > 2:
            factors.add(n)
        return factors

    def generate_safe_prime(self, bit_length=64):
        """ Generate a random safe prime number of specified bit length """
        while True:
            q = random.getrandbits(bit_length - 1)
            q |= (1 << (bit_length - 2)) | 1  # Ensure q has the desired bit length and is odd
            if self.is_prime(q):
                p = 2 * q + 1
                if self.is_prime(p):
                    return p

    def mod_pow(self, base, exp, mod):
        """ Modular exponentiation """
        result = 1
        while exp > 0:
            if exp & 1:
                result = (result * base) % mod
            exp >>= 1
            base = (base * base) % mod
        return result

    def encrypt(self, p, g, y, message):
        """ Encrypt a message using ElGamal encryption """
        k = random.randint(1, p - 2)
        c1 = self.mod_pow(g, k, p)
        s = self.mod_pow(y, k, p)
        ciphertext = []
        for char in message:
            ciphertext.append((ord(char) * s) % p)
        return c1, ciphertext

    def decrypt(self, p, x, c1, ciphertext):
        """ Decrypt a message using ElGamal decryption """
        s = self.mod_pow(c1, x, p)
        plaintext = ''
        for char_code in ciphertext:
            plaintext += chr((char_code * self.mod_pow(s, p - 2, p)) % p)
        return plaintext

# Example usage
elgamal = Gamal()
p = elgamal.generate_safe_prime()
g = elgamal.find_primitive_root(p)
x = random.randint(1, p - 1)  # Private key
y = elgamal.mod_pow(g, x, p)  # Public key

message = "Hello, world!"
print("Original message:", message)

c1, ciphertext = elgamal.encrypt(p, g, y, message)
print("Encrypted message:", (c1, ciphertext))

decrypted_message = elgamal.decrypt(p, x, c1, ciphertext)
print("Decrypted message:", decrypted_message)
