import logging
import socket

HOST = 'localhost'
PORT = 12345

logging.basicConfig(level=logging.DEBUG)


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
    user_input = input(f'>> {data}')
    user_input = ' ' if user_input == '' else user_input.strip()[:4].rjust(4, '0')
    s.send(str.encode(user_input))

    # room arrangement result, room wel msg
    for i in range(0, 2):
        data = s.recv(1024).decode()
        print(f'>> {data}')

    while True:
        data = s.recv(1024).decode()
        if len(data) == 0:
            break

        if data.find('letter?') == -1:
            print(f'>> {data}')
        else:
            user_input = input(f'>> {data}')
            user_input = ' ' if user_input == '' else user_input.strip()[:1]
            s.send(str.encode(user_input))


if __name__ == '__main__':
    socket_client()
