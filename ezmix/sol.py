def xor(a, array):
    for index, data in enumerate(array):
        array[index] = data ^ a
    return array

def add_reverse(a, array):
    for index, data in enumerate(array):
        array[index] = data - a
        if array[index] < 0:
            array[index] += 0x100
    return array

def shift_reverse(a, array):
    for index, data in enumerate(array):
        array[index] = (data << (a & 7) | data >> (8 - (a & 7))) & 0xff
        print(array[index])
    return array

def vm_machine(vm_num_array, data_array, output_array):
    for index, vm_num in enumerate(vm_num_array):
        if vm_num == 1:
            output_array = add_reverse(data_array[index], output_array)
        elif vm_num == 2:
            output_array = xor(data_array[index], output_array)
        else:
            output_array = shift_reverse(data_array[index], output_array)
    return output_array
        

def process_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    even_index_bytes = data[0::2]
    odd_index_bytes = data[1::2]

    vm_num = list(even_index_bytes[::-1])
    data = list(odd_index_bytes[::-1])
    
    vm_num.pop()
    data.pop()
        
    return vm_num, data

def read_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    data = list(data)
    return data

vm_num, data = process_file('program.bin')
output_array = read_file('output.bin')
print("VM_NUM:", vm_num)
print("DATA:", data)
print("OUTPUT:", output_array)

input = vm_machine(vm_num, data, output_array)
print(input)
input_string = ''.join([chr(i) for i in input])
print(input_string)

