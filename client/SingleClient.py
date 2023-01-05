import random
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

    # hello message, ask for room number
    data = s.recv(1024).decode()
    user_input = input(data)
    user_input = ' ' if user_input == '' else user_input.strip()[:4].rjust(4, '0')
    s.send(str.encode(user_input))

    # room arrangement result
    data = s.recv(1024).decode()
    print(f'>> {data}')

    # room welcome msg
    data = s.recv(1024).decode()
    print(f'>> {data}')

    s.close()


if __name__ == '__main__':
    socket_client()
