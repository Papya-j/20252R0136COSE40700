from z3 import *

def read_bytes_to_arrays(file_path):
    array1, array2, array3 = None, None, None  # 각각의 배열 초기화
    try:
        with open(file_path, 'rb') as file:  # 바이너리 모드로 파일 열기
            array1 = file.read(1000)  # 첫 번째 1000바이트 읽기
            array2 = file.read(1000)  # 두 번째 1000바이트 읽기
            array3 = file.read(1000)  # 세 번째 1000바이트 읽기

        # 배열의 크기를 확인 (총 3000바이트를 읽었다고 가정)
        if any(arr is None or len(arr) != 1000 for arr in [array1, array2, array3]):
            raise ValueError("파일 크기가 3000바이트가 아닙니다.")
        
         # -> array1, 2, 3 int형으로 변경
        array1 = [int(b) for b in array1]
        array2 = [int(b) for b in array2]
        array3 = [int(b) for b in array3]
        
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

    return array1, array2, array3

# 예제 파일 경로 (파일 이름 또는 경로를 변경하세요)
file_path = 'challenge.txt'
array1, array2, array3 = read_bytes_to_arrays(file_path)

def solve_check_with_groups(array1, array2, array3):
    # Define a 10x10x10 binary matrix for check_array
    check_array = [Int(f"check_array_{i}_{j}_{k}") for i in range(10) for j in range(10) for k in range(10)]
    solver = Solver()

    # Add constraints: check_array values must be 0 or 1
    for cell in check_array:
        solver.add(Or(cell == 0, cell == 1))
        
    i = 0
    j = 0
    # Define groups for v3, v4, and v5
    check_value_idx_1 = []  # Along k-dimension
    check_value_idx_2 = []  # Along j-dimension
    check_value_idx_3 = []  # Along i-dimension

    for k in range(10):
        idx_array1 = 100 * k + 10 * i + j
        idx_array2 = 100 * i + 10 * k + j
        idx_array3 = 100 * i + 10 * j + k

        # check_value의 적절한 index에 해당하는 [10] 배열
        check_value_idx_1.append(check_array[idx_array1])
        check_value_idx_2.append(check_array[idx_array2])
        check_value_idx_3.append(check_array[idx_array3])

    # array1, 2, 3의 [10]값 가져오기
    array1_values = [array1[100 * i + 10 * j + x] for x in range(10)]
    array2_values = [array2[100 * i + 10 * j + x] for x in range(10)]
    array3_values = [array3[100 * i + 10 * j + x] for x in range(10)]
    
    # array1, 2, 3의 총 합 = check_value의 총 합 (1의 개수 같아야 함)
    solver.add(Sum(check_value_idx_1) == Sum([array1_values[x] for x in range(10)]))
    solver.add(Sum(check_value_idx_2) == Sum([array2_values[x] for x in range(10)]))
    solver.add(Sum(check_value_idx_3) == Sum([array3_values[x] for x in range(10)]))
    
    # array1_values = [2, 3, 1, 0 ..] -> 0이 나오는 index = v6, v7, v8
    zero_idx_array1 = array1_values.index(0) if 0 in array1_values else 10
    zero_idx_array2 = array2_values.index(0) if 0 in array2_values else 10
    zero_idx_array3 = array3_values.index(0) if 0 in array3_values else 10
    
    print(solver.model())
    
    if solver.check() == sat:
        model = solver.model()
        
        evaluated_check_value_idx_1 = [model.eval(val).as_long() for val in check_value_idx_1]
        evaluated_check_value_idx_2 = [model.eval(val).as_long() for val in check_value_idx_2]
        evaluated_check_value_idx_3 = [model.eval(val).as_long() for val in check_value_idx_3]

        # 연속된 1의 개수를 세는 함수
        def count_consecutive_ones(arr):
            counts = []
            count = 0
            for val in arr:
                if val == 1:
                    count += 1
                else:
                    if count > 0:
                        counts.append(count)
                    count = 0
            if count > 0:
                counts.append(count)
            return counts
        
        num_groups_1 = len(count_consecutive_ones(evaluated_check_value_idx_1))
        num_groups_2 = len(count_consecutive_ones(evaluated_check_value_idx_2))
        num_groups_3 = len(count_consecutive_ones(evaluated_check_value_idx_3))
        
        # 1의 묶음 수가 같은지 확인
        solver.add(zero_idx_array1 == num_groups_1)
        solver.add(zero_idx_array2 == num_groups_2)
        solver.add(zero_idx_array3 == num_groups_3)
        
        # 연속된 1의 개수가 같은지 확인
        solver.add(array1_values[:num_groups_1] == count_consecutive_ones(evaluated_check_value_idx_1))
        solver.add(array2_values[:num_groups_2] == count_consecutive_ones(evaluated_check_value_idx_2))
        solver.add(array3_values[:num_groups_3] == count_consecutive_ones(evaluated_check_value_idx_3))
        
                
                
    if solver.check() == sat:
        model = solver.model()
        result = [[[model[check_array[100 * i + 10 * j + k]].as_long() for k in range(10)] for j in range(10)] for i in range(10)]
        return result
    else:
        return None

check_array = solve_check_with_groups(array1, array2, array3)

print(check_array)

for layer in check_array:
    for row in layer:
        print(''.join(map(str, row)))
    print()