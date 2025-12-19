import struct
import hashlib
import itertools
import string

hex_values = [
    0xFE5D3A093968D02B,
    0xBA0AA367C2862EAE,
    0x8BEA2ADA9E26604F,
    0x2E6F41C96DCF5224,
    0x7FD91BD2949B75F3,
    0x05B1ED8E6072F3A6,
    0xC94045C6D4887611,
    0x9D43DF6DF6B94D95,
    0xB9A8A83C8AC08D80,
    0x6D78E80376518464,
    0xE81A20F2023C2D0,
    0x2E41EAE69D89F186,
    0x425C831DD2A3E5FD,
    0x82788DBBDC4100EC,
    0x6D0FEE8D3901DD20,
    0xEBE82A0A41E5D783,
    0x2AFA26414B72E506,
    0xD1848E9C21D114D
]

new_array = []

for i in range(0, len(hex_values), 2):
    if i + 1 < len(hex_values):
        # Convert to little endian and concatenate
        first = struct.pack('<Q', hex_values[i]).hex()
        second = struct.pack('<Q', hex_values[i + 1]).hex()
        new_array.append(first + second)

def brute_force_md5(target_hash):
    chars = string.ascii_letters + string.digits + string.punctuation
    for guess in itertools.product(chars, repeat=3):
        guess_str = ''.join(guess)
        guess_hash = hashlib.md5(guess_str.encode()).hexdigest()
        if guess_hash == target_hash:
            return guess_str
    return None


flag = ''
for hash_str in new_array:
    result = brute_force_md5(hash_str)
    if result:
        flag += result
    
print(flag)