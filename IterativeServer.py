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

        with conn:
            print(f'Accepted connection from {addr}')
            conn.send(str.encode('Hello! You are now connected to the iterative sever'))

            while True:
                data = conn.recv(1024).decode()

                if not data:
                    break

                print(f'> Data from client: {data}')
                conn.send(f'You said "{data}"'.encode())

        conn.close()
        print(f'Conn from {addr} closed')


if __name__ == '__main__':
    start_iterative_server()
