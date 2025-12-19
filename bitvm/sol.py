def file_to_int_array(filepath):
    with open(filepath, 'rb') as file:
        content = file.read()
        int_array = [byte for byte in content]
        return int_array


command_array = file_to_int_array('command')
cal_command = command_array[0x9c:]

# transfer to readable command
# + extract the number

extract_number = []
i = 0
while i < len(cal_command):
    if cal_command[i] == 0x20:
        break
    elif cal_command[i] == 0x23:
        print(f"mov arr[{cal_command[i+1]}] {hex(cal_command[i+2])}")
        extract_number.append(cal_command[i+2])
        i += 3
    elif cal_command[i] == 0x24:
        print(f"mov arr[{cal_command[i+1]}] arr[{cal_command[i+2]}]")
        i += 3
    elif cal_command[i] == 0x25:
        print(f"and arr[{cal_command[i+1]}], arr[{cal_command[i+2]}] arr[{cal_command[i+3]}]")
        i += 4
    elif cal_command[i] == 0x26:
        print(f"or arr[{cal_command[i+1]}], arr[{cal_command[i+2]}] arr[{cal_command[i+3]}]")
        i += 4
    elif cal_command[i] == 0x27:
        print(f"xor arr[{cal_command[i+1]}], arr[{cal_command[i+2]}] arr[{cal_command[i+3]}]")
        i += 4
    elif cal_command[i] == 0x28:
        print(f"pop stack input to arr[0]")
        i += 1
    else:
        print(f"push {cal_command[i+1]}")
        i += 1

# {(x | arr[1]) ^ arr[3]} | {(x & arr[1]) ^ arr[2]} | arr[7] ... = 0
# x | arr[1] == arr[3] AND x & arr[1] == arr[2]

j = 0
input = []
while j < len(extract_number):
    for i in range(256):
        if (i | extract_number[j]) ==  extract_number[j+2] and (i & extract_number[j]) == extract_number[j+1]:
            input.append(i)
            break
    j += 3
    
    
print(''.join([chr(i) for i in input[::-1]]))