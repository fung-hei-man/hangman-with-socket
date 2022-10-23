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

    # greeting
    data = s.recv(1024).decode()
    print(f'> Data from server: {data}')

    client_idx = str(random.randint(0, 1000)).rjust(4, '0')
    send_and_recv_msg(s, f'Hello server, I am client #{client_idx}')

    # user message
    msg = ''
    while msg.strip().lower() != 'bye':
        msg = input(f'[Client {client_idx}] Input message to server: ')
        send_and_recv_msg(s, msg)

    s.close()


def send_and_recv_msg(socket, msg):
    socket.send(str.encode(msg))
    res = socket.recv(1024).decode()
    print(f'> Data from server: {res}')


if __name__ == '__main__':
    socket_client()
