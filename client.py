import socket

HOST = 'localhost'
PORT = 12345


def socket_client():
    try:
        s = socket.socket()
        s.connect((HOST, PORT))
    except socket.error as e:
        print('Oops! Something wrong when connecting to server')
        print(str(e))
        return

    data = s.recv(1024).decode()
    print(f'> Date from server: {data}')

    s.send(str.encode('Hello server'))
    data = s.recv(1024).decode()
    print(f'> Date from server: {data}')

    s.close()


if __name__ == '__main__':
    socket_client()
