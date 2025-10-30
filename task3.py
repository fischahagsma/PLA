import sympy as sp
import random

message = "семь"
message_index = "10001001010110011100"
message_index_list = ["1000", "1001", "0101", "1001", "1100"]

G = sp.Matrix([[1, 0, 0, 0, 0, 1, 1],
               [0, 1, 0, 0, 1, 0, 1],
               [0, 0, 1, 0, 1, 1, 0],
               [0, 0, 0, 1, 1, 1, 1]])
H = sp.Matrix([[0, 1, 1, 1, 1, 0, 0],
                [1, 0, 1, 1, 0, 1, 0],
                [1, 1, 0, 1, 0, 0, 1]])

def strings_to_column_matrices(strings):
    matrices = []
    for s in strings:
        col = sp.Matrix([[int(ch)] for ch in s])
        matrices.append(col)
    return matrices


def column_matrices_to_strings(matrices):

    strings = []
    for m in matrices:
        if m.cols != 1:
            raise ValueError("Все матрицы должны быть одностолбцовыми (n×1).")
        s = ''.join(str(int(x)) for x in m)
        strings.append(s)
    return strings

def split_by_4(s):
    return [s[i:i+4] for i in range(0, len(s), 4)]


def split_by_7(s):
    return [s[i:i+7] for i in range(0, len(s), 7)]


def flip_bits(s, positions):
    chars = list(s)
    for i in positions:
        chars[i] = '1' if chars[i] == '0' else '0'
    return ''.join(chars)


def matrix_to_latex(matrix):
    rows, cols = matrix.shape
    s = "\\begin{bmatrix}\n"
    for i in range(rows):
        s += " & ".join(str(int(matrix[i, j])) for j in range(cols))
        s += " \\\\\n"
    s += "\\end{bmatrix}"
    return s

def syndrome_latex(H, codeword, block_index=1):
    syndrome = (H * codeword).applyfunc(lambda x: x % 2)
    latex_str = f"\\[\nz_{{{block_index}}} = \n"
    latex_str += matrix_to_latex(H) + "\n"
    latex_str += matrix_to_latex(codeword) + "\n= \n"
    latex_str += matrix_to_latex(syndrome) + "\n\\]\n"
    return latex_str


p = strings_to_column_matrices(message_index_list)
c = [(G.T * m).applyfunc(lambda x: x % 2) for m in p]
s = "".join(column_matrices_to_strings(c))

s1 = flip_bits(s, positions=[33])
s2 = flip_bits(s, positions=[30, 23])
s3 = flip_bits(s, positions=[28, 31, 1])
s4 = flip_bits(s, positions=[5, 20, 13, 29])
p1 = strings_to_column_matrices(split_by_7(s4))

print("Блок с ошибкой:")
print(p1[4])
print("Нужное:")
print((H * p1[0]).applyfunc(lambda x: x % 2))


def compute_syndrome(H, codeword):
    return (H * codeword).applyfunc(lambda x: x % 2)

def error_correction(H, codeword):
    syndrome = compute_syndrome(H, codeword)

    if all(int(x) == 0 for x in syndrome):
        correction = sp.zeros(codeword.rows, 1)
        return correction, codeword.copy(), syndrome
    
    error_pos = None
    for j in range(H.cols):
        col = H[:, j].applyfunc(int)
        if list(col) == [int(x) for x in syndrome]:
            error_pos = j 
    
    if error_pos is None:
        raise ValueError("Ошибка: синдром не соответствует ни одной колонке H.")
    

    correction = sp.zeros(codeword.rows, 1)
    correction[error_pos, 0] = 1
    corrected_codeword = (codeword + correction).applyfunc(lambda x: x % 2)
    return correction, corrected_codeword, syndrome



correction, corrected_codeword, syndrome = error_correction(H, p1[4])

print("Синдром:")
print(syndrome)
print("\nКоррекция:")
print(correction)
print("\nИсправленное кодовое слово:")
print(corrected_codeword)



corrected_blocks = []
error_info = []  

for i, block in enumerate(p1):
    correction, corrected, syndrome = error_correction(H, block)
    corrected_blocks.append(corrected)
    
    
    if any(int(x) != 0 for x in syndrome):
        pos = next(j+1 for j, x in enumerate(correction) if int(x) == 1)
        error_info.append((i, pos, syndrome))


for info in error_info:
    block_idx, pos, synd = info
    print(f"Ошибка в блоке {block_idx}, позиция {pos} (1-based)")
    print("Синдром:")
    print(synd)
    print("---")

print("Исправленные блоки:")
for blk in corrected_blocks:
    print(blk.T)  

