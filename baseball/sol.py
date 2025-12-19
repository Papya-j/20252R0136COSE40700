# [1] : table_filename = 64개, byte_4040 -> 65개
# [2] : input_filename = 개수 모름. s에 할당
# [3] : ptr 값이 답 -> sub_1289(s, size(input_filename))

# 종합적으로 base64의 원리를 따름

#!/usr/bin python3

import base64

# Given inputs
text_in = "Pepero is a cookie stick, dipped in compound chocolate, manufactured by lotte Confectionery in South Korea\nPepero Day is held annually on November 11"
text_out = "7/OkZQIau/jou/R1by9acyjjutd0cUdlWshecQhkZUn1cUH1by9g4/9qNAn1byGaby9pbQSjWshgbUmqZAF+JtOBZUn1b8e1YoMPYoM1ny95ZAO+J/jaNAOB2vhrNLhVNDO0cshWNDIjbnrnZQhj4AM1S/Fmu/jou/GjN/n1bUm5JUFpNte1NyH1VA9yZUqLZQu13VR="
flag_out = "S/jeutjaJvhlNA9Du/GaJBhLbQdjd+n1Jy9BcD3="

# standard_encode = text_in을 byte로 변환 후 base64.b64encode 통해 인코딩, 이후 바이트를 decode로 문자열로 변환
encoded_standard = base64.b64encode(text_in.encode()).decode()

# 2. 커스텀 테이블 추출
custom_table = [0] * 64  # Base64 테이블은 64개의 값으로 구성
standard_base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# 표준 Base64와 text_out 비교를 통해 매핑 생성
for standard_char, custom_char in zip(encoded_standard, text_out):
    if custom_char not in custom_table:
        index = standard_base64_chars.find(standard_char)
        if index != -1:
            custom_table[index] = custom_char

# 3. 커스텀 테이블 완성
# 아직 채워지지 않은 값들을 처리
for i, char in enumerate(custom_table):
    if char == 0:
        custom_table[i] = '?'

# 4. 결과 출력
#print("Custom Table:", ''.join(custom_table))

custom_table_int = [ord(char) for char in custom_table]

reverse_table = {chr(value): index for index, value in enumerate(custom_table_int) if value != 0}
#print(reverse_table)

# Decode the flag_out using the reverse table
decoded_bits = []
for char in flag_out:
    if char in reverse_table:  # Ignore characters not in the table
        decoded_bits.append(reverse_table[char])
#print(decoded_bits)
# Group the decoded bits into 8-bit chunks and convert to characters
decoded_bytes = []
i = 0
while i + 3 < len(decoded_bits):  # Process only full groups of 4
    b = (decoded_bits[i] << 2) | (decoded_bits[i + 1] >> 4)
    decoded_bytes.append(b)
    b = ((decoded_bits[i + 1] & 0xF) << 4) | (decoded_bits[i + 2] >> 2)
    decoded_bytes.append(b)
    b = ((decoded_bits[i + 2] & 0x3) << 6) | decoded_bits[i + 3]
    decoded_bytes.append(b)
    i += 4

# Handle any remaining bits (if the length of decoded_bits is not a multiple of 4)
if len(decoded_bits) % 4 == 2:
    b = (decoded_bits[i] << 2) | (decoded_bits[i + 1] >> 4)
    decoded_bytes.append(b)
elif len(decoded_bits) % 4 == 3:
    b = (decoded_bits[i] << 2) | (decoded_bits[i + 1] >> 4)
    decoded_bytes.append(b)
    b = ((decoded_bits[i + 1] & 0xF) << 4) | (decoded_bits[i + 2] >> 2)
    decoded_bytes.append(b)

# Convert bytes to string
decoded_string = ''.join(chr(b) for b in decoded_bytes if b != 0)
print("Decoded String:", decoded_string)