from pwn import *


#p = process('./prob')
p = remote('host1.dreamhack.games', 15522)
context.log_level = 'debug'

def slog(n, m): return success(": ".join([n, hex(m)]))

for i in range(10):
    p.recvuntil(b'[INFO]')  # '[INFO]'까지 데이터를 읽음

    # '[INFO]' 이후 데이터 수신
    info_output = p.recvline().decode('utf-8').strip()

    # 데이터 파싱
    info_parts = info_output.split(',')
    stats = {part.split(':')[0].strip(): int(part.split(':')[1].strip()) for part in info_parts}

    # 출력 확인
    combined_value = (
        (stats.get('HP', 0) << 48) |  
        (stats.get('STR', 0)) | 
        (stats.get('DEX', 0)<<40 ) |  
        (stats.get('END', 0)<< 32 ) | 
        (stats.get('INT', 0)<< 24 ) |  
        (stats.get('VIT', 0)<< 16 ) |   
        (stats.get('AGI', 0)<< 8)          
    )

    slog('combined_value', combined_value)

    operation_sequence = []
    target = combined_value

    while target > 0:
        if target % 2 == 1:  # 홀수일 때 A를 추가
            operation_sequence.append('A')
            target -= 1
        else:  # 짝수일 때 B를 추가
            operation_sequence.append('B')
            target //= 2
    operation_sequence = ''.join(reversed(operation_sequence))
    p.sendlineafter('Cast your spell!: ', operation_sequence)



p.interactive()
