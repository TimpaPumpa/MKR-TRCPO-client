import socket
import struct
import pickle
import numpy as np
import random

HOST = '127.0.0.1'
PORT = 65434

def send_all(sock, data):
    sock.sendall(data)

def run_client():
    # 1. Генеруємо розміри
    N = random.randint(1001, 1100)
    M = random.randint(1001, 1100)
    L = random.randint(1001, 1100)

    # 2. Генеруємо матриці
    mat1 = np.random.randint(0, 10, size=(N, M))  # матриця N x M
    mat2 = np.random.randint(0, 10, size=(M, L))  # матриця M x L

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # 3. Відправляємо розміри
        s.sendall(struct.pack('!iii', N, M, L))

        # 4. Відправляємо матриці (через pickle)
        pickled_mat1 = pickle.dumps(mat1)
        s.sendall(struct.pack('!i', len(pickled_mat1)))
        s.sendall(pickled_mat1)

        pickled_mat2 = pickle.dumps(mat2)
        s.sendall(struct.pack('!i', len(pickled_mat2)))
        s.sendall(pickled_mat2)

        # 5. Приймаємо результат
        #    Спочатку 4 байти розміру
        raw_length = s.recv(4)
        result_length = struct.unpack('!i', raw_length)[0]
        result_data = b''
        while len(result_data) < result_length:
            chunk = s.recv(result_length - len(result_data))
            if not chunk:
                break
            result_data += chunk
        result_matrix = pickle.loads(result_data)

        # Перевірка, що розмір (N, L)
        print(f"Розмір отриманої матриці: {result_matrix.shape}")
        # Можемо вивести перші 5x5 елементів
        print(result_matrix[:5, :5])

if __name__ == "__main__":
    run_client()
