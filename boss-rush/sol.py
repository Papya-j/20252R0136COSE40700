from pwn import *
import itertools


context.log_level = 'debug'

#'''
# 세 번째 행의 가능한 모든 경우의 수 생성
third_row_possibilities = [''.join(row) for row in itertools.permutations('OXXXX')]

# 나머지 행의 가능한 모든 경우의 수 생성
other_rows_possibilities = [''.join(row) for row in itertools.product('OX', repeat=5)]

# 가능한 모든 5x5 매트릭스 생성 및 전송
for third_row in third_row_possibilities:
    for row1 in other_rows_possibilities:
        for row2 in other_rows_possibilities:
            for row4 in other_rows_possibilities:
                for row5 in other_rows_possibilities:
                    matrix = f"{row1}\n{row2}\n{third_row}\n{row4}\n{row5}"
                    p = process('./main')
                    p.sendlineafter('> ', b'2')
                    p.recvuntil('Insert password pattern:')
                    p.sendline(matrix)
                    p.recvline()
                    result = p.recvline()
                    if b"Loaded from password!" in result:
                        print(matrix)
                        a = p.recvuntil('> ')
                        with open('successful_matrix.txt', 'a') as f:
                            f.write(f"Matrix:\n{matrix}\n")
                            f.write(f"Response:\n{a.decode()}\n")
                        p.close()
                    elif b"No cheating!" in result:
                        p.close()
#'''                
                        
'''
                    
p = process('./main')
p.sendlineafter('> ', b'2')
p.recvuntil('Insert password pattern:')
matrix = f"OXOXO\nXOXOX\nOXXXX\nXOXOX\nOXOXO"
p.sendline(matrix)
p.recvline()
result = p.recvline()
print(result)
if b"Loaded from password!" in result:
    print("Success:", matrix)
    p.interactive()
elif b"No cheating!" in result:
    print("Failed:", matrix)
    p.close()


'''        