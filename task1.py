import sympy as sp
import random

russian_letters = list("приветм")
extras = [" ", "."]
alphabet = russian_letters + extras

char_to_index = {ch: i for i, ch in enumerate(alphabet)}
index_to_char = {i: ch for i, ch in enumerate(alphabet)}
print(len(alphabet))
print(alphabet)
message = "привет мир ."
message_index = [char_to_index[i] for i in message]

A = sp.Matrix([[1, 3],  #2
              [2,8]])
B = sp.Matrix([[1,2,3], #8
              [0,1,4],
              [5,6,7]])
C = sp.Matrix([[1,2,3,4], #4
              [0,1,2,3],
              [1,0,1,0],
              [2,1,0,1]])


def CharToIndex(message, alphabet):
    char_to_index = {ch: i for i, ch in enumerate(alphabet)}
    return [char_to_index[i] for i in message]

def IndexToChar(message_index, alphabet):
    index_to_char = {i: ch for i, ch in enumerate(alphabet)}
    return ''.join([index_to_char[i] for i in message_index])

def hill_encrypt(K, P, n):
    a = K.shape[0]
    C = []
    bloks = [sp.Matrix(P[i:i+a]) for i in range(0, len(P), a)]
    for b in bloks:
        C.append(((K * b) % n))
    C = sp.Matrix.vstack(*C)
    return C

def hill_decrypt(K, C, n):
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

def make3Errors(message):
    message = list(message)
    indexes = random.sample(range(len(message)), 3)
    for i in indexes:
        message[i] = random.choice(alphabet)
    return ''.join(message)


print("Исходное сообщение: ", message)
print("Индексное представление: ", message_index)


for mat in [A, B, C]:
    print("\nМатрица ключа:\n", mat)
    temp = MatrixToList(hill_encrypt(mat, message_index, len(alphabet)))
    encryptMessage = IndexToChar(MatrixToList(hill_encrypt(mat, message_index, len(alphabet))), alphabet)
    encryptMessageWithErrors = make3Errors(encryptMessage)
    decryptedMeassage = IndexToChar(MatrixToList(hill_decrypt(mat, CharToIndex(encryptMessage, alphabet), len(alphabet))), alphabet)
    decryptedMessageWithErrors = IndexToChar(MatrixToList(hill_decrypt(mat, CharToIndex(encryptMessageWithErrors, alphabet), len(alphabet))), alphabet)
    print("Зашифрованное сообщение: ", encryptMessage)
    print("Зашифрованное сообщение в цифрах: ", temp)
    print("Зашифрованное сообщение с 3 ошибками: ", encryptMessageWithErrors)
    print("Расшифрованное сообщение: ", decryptedMeassage)
    print("Зашифрованное сообщение с ошибками: ", encryptMessageWithErrors)
    print("Расшифрованное сообщение c ошибками: ", decryptedMessageWithErrors)
