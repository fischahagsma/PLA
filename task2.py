try:
    import sympy as sp
except Exception:
    sp = None
import random

russian_letters = list("приветм")
extras = [" ", "."]
alphabet = russian_letters + extras


P = sp.Matrix([[0, 2],
               [1, 3]])

C = sp.Matrix([[3, 2],
               [8, 1]])


def CharToIndex(message, alphabet):
    char_to_index = {ch: i for i, ch in enumerate(alphabet)}
    return [char_to_index[i] for i in message]

def IndexToChar(message_index, alphabet):
    index_to_char = {i: ch for i, ch in enumerate(alphabet)}
    return ''.join([index_to_char[i] for i in message_index])

def hill_encrypt(K, P, n):
    if sp is None:
        raise RuntimeError("sympy не установлен — hill_encrypt недоступна")
    a = K.shape[0]
    C = []
    bloks = [sp.Matrix(P[i:i+a]) for i in range(0, len(P), a)]
    for b in bloks:
        C.append(((K * b) % n))
    C = sp.Matrix.vstack(*C)
    return C

def hill_decrypt(K, C, n):
    if sp is None:
        raise RuntimeError("sympy не установлен — hill_decrypt недоступна")
    a = K.shape[0]
    K_inv = K.inv_mod(n)
    P = []
    bloks = [sp.Matrix(C[i:i+a]) for i in range(0, len(C), a)]
    for b in bloks:
        P.append(((K_inv * b) % n))
    P = sp.Matrix.vstack(*P)
    return P

def MatrixToList(M):
    return M.T.tolist()[0]

def random_quad(max_product=1000, min_val=1):
    while True:
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        c = random.randint(1, 100)
        denom = a * b * c
        if denom == 0:
            continue
        max_d = (max_product - 1) // denom
        for _ in range(10):
            d = random.randint(1, 100)
            if (a * d - b * c) % 3 != 0:
                return a, b, c, d
        for d in range(min_val, max_d + 1):
            if (a * d - b * c) % 3 != 0:
                return a, b, c, d




#    a, b, c, d = random_quad()
#    prod4 = a * b * c * d
#    print(f"Сгенерированы числа (четверка): {a}, {b}, {c}, {d}")
#    print(f"Разность a*d - b*c = {a*d - b*c}, по модулю 9 равно {(a*d - b*c) % 9}")
#    assert (a * d - b * c) % 3 != 0, "Разность произведений не должна быть кратна 3"

a, b, c, d = random_quad()
K = sp.Matrix([[a, b],
               [c, d]])
K = K % len(alphabet)
K = sp.Matrix([[2, 4],
               [8, 2]])

P = sp.Matrix([[0, 1],
               [2, 7]]) 
message1 = "пир тир вир."
message2 = "рим и ветер."
message1_index = CharToIndex(message1, alphabet)
message1_encrypt = MatrixToList(hill_encrypt(K, message1_index, len(alphabet)))
message2_index = CharToIndex(message2, alphabet)
message2_encrypt = MatrixToList(hill_encrypt(K, message2_index, len(alphabet)))
print("Матрица ключа:\n", K)
print("Зашифрованное сообщение 1 в цифрах: ", message1_encrypt)
print("Расшифрованное сообщение 1: ", CharToIndex(message1, alphabet))
print("Расшифрованное сообщение 1: ", IndexToChar(MatrixToList(hill_decrypt(K, message1_encrypt, len(alphabet))), alphabet))
print("Зашифрованное сообщение 2 в цифрах: ", message2_encrypt)
print("Расшифрованное сообщение 2: ", IndexToChar(MatrixToList(hill_decrypt(K, message2_encrypt, len(alphabet))), alphabet))
print("Расшифрованное сообщение 2: ", CharToIndex(message2, alphabet))



