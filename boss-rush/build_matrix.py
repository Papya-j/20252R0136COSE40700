import itertools
from pwn import *

context.log_level = 'debug'

some_num= [0xB0000000F, 0x300000005, 0x400000006, 0x1200000011, 0x100000007, 0xE00000000, 0x130000000A, 0xD00000009]


# 세 번째 행의 가능한 모든 경우의 수 생성
third_row_possibilities = [''.join(row) for row in itertools.permutations('OXXXX')]

# 나머지 행의 가능한 모든 경우의 수 생성
other_rows_possibilities = [''.join(row) for row in itertools.product('OX', repeat=5)]

def matrix_to_bits(matrix):
    bit_string = ""
    # MSB부터 두번째, 네번째, 마지막, 첫번째 줄로 5개씩 순서대로 나열
    for row in [matrix[1], matrix[3], matrix[4], matrix[0]]:
        for char in reversed(row):
            bit_string += '1' if char == 'O' else '0'
    return bit_string

def shift_bits(int_string, shift):
    return ((int_string >> shift) | (int_string << (20 - shift))) & 0xFFFFF


# 가능한 모든 5x5 매트릭스 생성 및 비트 변환
for third_row in third_row_possibilities:
    for row1 in other_rows_possibilities:
        for row2 in other_rows_possibilities:
            for row4 in other_rows_possibilities:
                for row5 in other_rows_possibilities:
                    matrix = [row1, row2, third_row, row4, row5]
                    bit_string = matrix_to_bits(matrix)
                    int_string = int(bit_string, 2)
                    m = third_row.index('O')
                    result_bit = shift_bits(int_string, m)
                    temp = 0
                    for num in some_num:
                        lsb = num & 0xFF
                        sbyte4 = (num >> 32) & 0xFF
                        if ((result_bit & (1<<lsb)) != 0) == ((result_bit & (1<<sbyte4)) != 0):
                            break
                        if result_bit & (1<<sbyte4) == 0:
                            break
                        temp+=1
                    if temp == len(some_num):
                        #print(f"Matrix:\n{row1}\n{row2}\n{third_row}\n{row4}\n{row5}\n")
                        matrix = f"{row1}\n{row2}\n{third_row}\n{row4}\n{row5}"
                        #p = process('./main')
                        p = remote('host3.dreamhack.games', 20634)
                        p.sendlineafter('> ', b'2')
                        p.recvuntil('Insert password pattern:')
                        p.sendline(matrix)
                        temp_1 = 0
                        while(1):
                            p.sendlineafter('> ', '1')
                            dump_1 = p.recvline()
                            dump_2 = p.recvline()
                            a = p.recvline()
                            if b'Big Slime defeated!\n' == a:
                                break
                            p.sendlineafter('> ', '2')
                            b = p.recvline()
                            if b'Not enough potion!\n' == b:
                                temp_1 = 1
                                p.close()
                                break
                        if temp_1 == 1:
                            continue
                        result = p.recvline()
                        print(f"result: {result}")
                        if b'Cannot open flag file!\n' == result:
                            print(result)
                            p.close()
                            continue
                        else:
                            print(result)
                            print(f"Matrix:\n{row1}\n{row2}\n{third_row}\n{row4}\n{row5}\n")
                            p.interactive()






    
    