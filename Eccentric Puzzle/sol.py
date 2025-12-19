from z3 import *

# challenge.txt 파일 읽어서 3개의 배열로 변환환
def read_bytes_to_arrays(file_path):
    array1, array2, array3 = None, None, None
    try:
        with open(file_path, 'rb') as f:
            data1 = f.read(1000)
            data2 = f.read(1000)
            data3 = f.read(1000)
            
        array1 = [int(b) for b in data1]
        array2 = [int(b) for b in data2]
        array3 = [int(b) for b in data3]

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

    return array1, array2, array3

file_path = "challenge.txt"
# 각각에 해당되는 배열
array1, array2, array3 = read_bytes_to_arrays(file_path)


def parse_run_spec(values):
    # [2, 3, 0, 0, 0, 0, 0, 0, 0, 0] -> [2, 3]로 뽑아내는 과정
    runs = []
    for v in values:
        if v <= 0:
            break
        runs.append(v)
    return runs


def add_nonogram_line_constraint(solver, line_vars, run_list, prefix=""):
    """
    line_vars: 길이 10인 Z3 Int 변수(각각 0 또는 1).
    run_list: 예) [2, 3] -> "길이2 짜리 1그룹, 길이3 짜리 1그룹"이라는 의미
    prefix: 디버깅용 이름(prefix)
    
    전형적인 Nonogram의 '한 줄' 제약을 추가한다.
    - 모든 line_vars[i]는 0 또는 1.
    - run_list가 비어있으면 => 전부 0
    - run_list가 있으면 => group들이 순서대로 배치, 그룹 간 최소 1칸의 0 간격.
    """
    N = len(line_vars) 

    # 만약 run_list가 비어있으면 => 전부 0
    if not run_list:
        for lv in line_vars:
            solver.add(lv == 0)
        return

    # run_list가 존재한다면, 각 run마다 시작 위치 start[r]를 정의
    # run_count = len(run_list)
    run_count = len(run_list)
    start_vars = [Int(f"{prefix}_start_{r}") for r in range(run_count)]

    # 각 start[r]에 대해 0 <= start[r] <= N-1
    for r in range(run_count):
        solver.add(start_vars[r] >= 0)
        solver.add(start_vars[r] < N)

    # 그룹 간 순서, 간격 제약
    # (예: start[r+1] >= start[r] + run_list[r] + 1)
    for r in range(run_count - 1):
        solver.add(start_vars[r+1] >= start_vars[r] + run_list[r] + 1)

    # 마지막 그룹이 범위를 넘어가지 않도록
    # start[r] + run_list[r] <= N
    for r in range(run_count):
        solver.add(start_vars[r] + run_list[r] <= N)

    # 이제 각 칸 i에 대해:
    # line_vars[i] == 1  <->  i가 어느 그룹 r의 [start[r], start[r]+run_list[r]) 범위 안에 속함
    # line_vars[i] == 0  <->  속하지 않음
    for i in range(N):
        in_any_group = []
        for r in range(run_count):
            # 조건: start[r] <= i < start[r] + run_list[r]
            in_group_r = And(start_vars[r] <= i, i < start_vars[r] + run_list[r])
            in_any_group.append(in_group_r)

        solver.add(line_vars[i] == If(Or(*in_any_group), 1, 0))


def solve_check_with_groups(array1, array2, array3):
    solver = Solver()

    # 10x10x10 = 1000개의 Int 변수(각각 0 또는 1)
    check_array = [Int(f"check_array_{i}_{j}_{k}") for i in range(10) for j in range(10) for k in range(10)]

    # 모든 cell은 0 또는 1
    for cell in check_array:
        solver.add(Or(cell == 0, cell == 1))
    
    for i in range(10):
        for j in range(10):
            #k방향
            line_k = []
            for k in range(10):
                idx_k = 100*k + 10*i + j
                line_k.append(check_array[idx_k])

            # array1에서의 run 스펙 (길이10 구간)
            array1_values = array1[100*i + 10*j : 100*i + 10*j + 10]
            # array1_values 간결화
            runs_k = parse_run_spec(array1_values)
            # 제약 추가
            add_nonogram_line_constraint(solver, line_k, runs_k, prefix=f"(i{i}_j{j})_dirK")

            #j방향
            line_j = []
            for k in range(10):
                idx_j = 100*i + 10*k + j  
                line_j.append(check_array[idx_j])
            array2_values = array2[100*i + 10*j : 100*i + 10*j + 10]
            runs_j = parse_run_spec(array2_values)
            add_nonogram_line_constraint(solver, line_j, runs_j, prefix=f"(i{i}_j{j})_dirJ")

            #i방향 (1번째 축)
            line_i = []
            for k in range(10):
                idx_i = 100*i + 10*j + k
                line_i.append(check_array[idx_i])
            array3_values = array3[100*i + 10*j : 100*i + 10*j + 10]
            runs_i = parse_run_spec(array3_values)
            add_nonogram_line_constraint(solver, line_i, runs_i, prefix=f"(i{i}_j{j})_dirI")

    if solver.check() == sat:
        model = solver.model()
        result = []
        for i in range(10):
            for j in range(10):
                for k in range(10):
                    idx = 100*i + 10*j + k
                    result.append(model[check_array[idx]].as_long())
        return result

check_array = solve_check_with_groups(array1, array2, array3)


# 1차원 배열을 input.txt 규칙에 따라 변환환
def build_input_array(check_array):

    result = bytearray()

    for line_index in range(10):
        for num in range(10):
            start_idx = line_index * 100 + num * 10
            chunk = check_array[start_idx : start_idx + 10]
            for val in chunk:
                if val == 1:
                    char_val = '1'
                else:
                    char_val = '0'
                result.append(ord(char_val)) 
            result.append(0x0A)
        for _ in range(10):
            result.append(0x2D)
        result.append(0x0A)

    return result

# input data 복구 (1000byte -> 1210byte)
input_data = build_input_array(check_array)

# input.txt 파일에 저장장
with open("input.txt", "wb") as f:
    f.write(input_data)