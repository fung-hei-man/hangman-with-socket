import re
import socket

PORT = 12345
QUEUE_SIZE = 5


def start_iterative_server():
    try:
        s = socket.socket()
        s.bind(('localhost', PORT))
        s.listen(QUEUE_SIZE)
    except socket.error as e:
        print('Oops! Something is wrong when try listening from socket')
        print(str(e))
        return

    print(f'Iterative server listening to port {PORT} with queue size {QUEUE_SIZE}')

    while True:
        conn, addr = s.accept()
        client_idx = None

        with conn:
            print(f'Accepted connection from {addr}')
            conn.send(str.encode('Hello! You are now connected to the iterative sever'))

            while True:
                data = conn.recv(1024).decode()

                if not data:
                    break
                elif client_idx is None:
                    reg_exp = re.match('Hello server, I am client #(\d+)', data)
                    if reg_exp is not None:
                        client_idx = reg_exp.group(1)

                print(f'> Data from client #{client_idx}: {data}')
                conn.send(f'You said "{data}"'.encode())

        print(f'Status of connection from {addr}: {"closed" if conn.fileno() == -1 else "connected"}')


if __name__ == '__main__':
    start_iterative_server()
