array = []
s = [0]*64
xor_count = 0

def Append(x):
    array.append(x)
    
def Input_to_Array():
    array[-1] = array[-1] + 300
    
def XOR():
    global xor_count
    xor_count += 1

def Compare_func():
    '''
    1) XOR이 없는 경우 -> Input_to_Array, Append만 존재
    2) XOR이 있는 경우 -> Input_to_Array, XOR(여러개), Append 순서로 존재
    XOR을 xor_count만 실행하는 만큼, array에서 append로 들어간 마지막 원소를 빼고 XOR 수행.
    마지막에서 두 번째 원소는 s에 대한 정보임
    
    ex, XOR 3번 호출, array[0]에서 시작했다 치면
    array[0~3] = 정상적인 값, array[4] = s에 대한 정보, array[5] = 최종 compare 값
    -> array[0] = 최종 compare 값
    -> xor_count-1만큼 돌아야 함. (최종 compare 값과 XOR을 수행해야 됨)
    '''
    global xor_count
    if xor_count == 0:
        s_index = array[-2] - 300
        s[s_index] = array[-1]
        array[-2] = s[s_index]
        array.pop()
    else:
        last_value = array[-1]
        array.pop()
        s_index = array[-1] - 300
        array.pop()
        for _ in range(xor_count-1):
            array[-2] ^= array[-1]
            array.pop()
        s[s_index] = array[-1] ^ last_value
        array[-1] = last_value
        xor_count = 0


Append(63)
Input_to_Array()  # array[0] = s[63]
Append(51)
Compare_func()  # s[63] == 51
Append(62)
Input_to_Array()  # array[1] = s[62]
XOR()  # array[0] ^= array[1]
Append(4)  # array[1] = 4
Compare_func()  # array[0] == 4
Append(61)
Input_to_Array()  # array[1] = s[61]
Append(101)
Compare_func()  # s[61] == 101
Append(60)
Input_to_Array()  # array[2] = s[60]
XOR()  # array[1] ^= array[2]
XOR()  # array[0] ^= array[1]
Append(80)
Compare_func()  # array[0] == 80
Append(59)
Input_to_Array()  # array[1] = s[59]
Append(102)
Compare_func()  # s[59] == 102
Append(58)
Input_to_Array()  # array[2] = s[58]
XOR()  # array[1] ^= array[2]
Append(82)
Compare_func()  # array[1] == 82
Append(57)
Input_to_Array()  # array[2] = s[57]
Append(52)
Compare_func()  # s[57] == 52
Append(56)
Input_to_Array()  # array[3] = s[56]
XOR()
XOR()
XOR()  # array[0] ^= arr[1], arr[2], arr[3]
Append(83)
Compare_func()  # array[0] == 83
Append(55)
Input_to_Array()  # array[1] = s[55]
Append(50)
Compare_func()  # s[55] == 50
Append(54)
Input_to_Array()  # array[2] = s[54]
XOR()
Append(87)
Compare_func()  # array[1] == 87
Append(53)
Input_to_Array()  # array[2] = s[53]
Append(52)
Compare_func()  # s[53] == 52
Append(52)
Input_to_Array()  # array[3] = s[52]
XOR()
XOR()  # array[1]
Append(91)
Compare_func()  # array[1] == 91
Append(51)
Input_to_Array()  # array[2] = s[51]
Append(57)
Compare_func()  # s[51] == 57
Append(50)
Input_to_Array()  # array[3] = s[50]
XOR()
Append(91)
Compare_func()  # array[2] == 91
Append(49)
Input_to_Array()  # array[3] = s[49]
Append(51)
Compare_func()  # s[49] == 51
Append(48)
Input_to_Array()  # array[4] = s[48]
XOR()
XOR()
XOR()
XOR()
Append(4)
Compare_func()  # array[0] ^ ~ arr[4] == 4
Append(47)
Input_to_Array()
Append(102)
Compare_func()
Append(46)
Input_to_Array()
XOR()
Append(7)
Compare_func()
Append(45)
Input_to_Array()
Append(56)
Compare_func()
Append(44)
Input_to_Array()
XOR()
XOR()
Append(10)
Compare_func()
Append(43)
Input_to_Array()
Append(99)
Compare_func()
Append(42)
Input_to_Array()
XOR()
Append(7)
Compare_func()
Append(41)
Input_to_Array()
Append(52)
Compare_func()
Append(40)
Input_to_Array()
XOR()
XOR()
XOR()
Append(90)
Compare_func()
Append(39)
Input_to_Array()
Append(53)
Compare_func()
Append(38)
Input_to_Array()
XOR()
Append(4)
Compare_func()
Append(37)
Input_to_Array()
Append(102)
Compare_func()
Append(36)
Input_to_Array()
XOR()
XOR()
Append(86)
Compare_func()
Append(35)
Input_to_Array()
Append(99)
Compare_func()
Append(34)
Input_to_Array()
XOR()
Append(6)
Compare_func()
Append(33)
Input_to_Array()
Append(50)
Compare_func()
Append(32)
Input_to_Array()
XOR()
XOR()
XOR()
XOR()
XOR()
Append(93)
Compare_func()
Append(31)
Input_to_Array()
Append(99)
Compare_func()
Append(30)
Input_to_Array()
XOR()
Append(6)
Compare_func()
Append(29)
Input_to_Array()
Append(52)
Compare_func()
Append(28)
Input_to_Array()
XOR()
XOR()
Append(5)
Compare_func()
Append(27)
Input_to_Array()
Append(99)
Compare_func()
Append(26)
Input_to_Array()
XOR()
Append(2)
Compare_func()
Append(25)
Input_to_Array()
Append(97)
Compare_func()
Append(24)
Input_to_Array()
XOR()
XOR()
XOR()
Append(81)
Compare_func()
Append(23)
Input_to_Array()
Append(97)
Compare_func()
Append(22)
Input_to_Array()
XOR()
Append(80)
Compare_func()
Append(21)
Input_to_Array()
Append(49)
Compare_func()
Append(20)
Input_to_Array()
XOR()
XOR()
Append(88)
Compare_func()
Append(19)
Input_to_Array()
Append(98)
Compare_func()
Append(18)
Input_to_Array()
XOR()
Append(84)
Compare_func()
Append(17)
Input_to_Array()
Append(51)
Compare_func()
Append(16)
Input_to_Array()
XOR()
XOR()
XOR()
XOR()
Append(88)
Compare_func()
Append(15)
Input_to_Array()
Append(53)
Compare_func()
Append(14)
Input_to_Array()
XOR()
Append(7)
Compare_func()
Append(13)
Input_to_Array()
Append(48)
Compare_func()
Append(12)
Input_to_Array()
XOR()
XOR()
Append(85)
Compare_func()
Append(11)
Input_to_Array()
Append(48)
Compare_func()
Append(10)
Input_to_Array()
XOR()
Append(82)
Compare_func()
Append(9)
Input_to_Array()
Append(100)
Compare_func()
Append(8)
Input_to_Array()
XOR()
XOR()
XOR()
Append(1)
Compare_func()
Append(7)
Input_to_Array()
Append(52)
Compare_func()
Append(6)
Input_to_Array()
XOR()
Append(3)
Compare_func()
Append(5)
Input_to_Array()
Append(100)
Compare_func()
Append(4)
Input_to_Array()
XOR()
XOR()
Append(83)
Compare_func()
Append(3)
Input_to_Array()
Append(100)
Compare_func()
Append(2)
Input_to_Array()
XOR()
Append(0)
Compare_func()
Append(1)
Input_to_Array()
Append(101)
Compare_func()
Append(0)
Input_to_Array()
XOR()
XOR()
XOR()
XOR()
XOR()
XOR()
Append(0)
Compare_func()


flag = ''.join([chr(x) for x in s])
print(f"Flag: {flag}")