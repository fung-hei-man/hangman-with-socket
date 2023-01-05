import socket
import threading

HOST = 'localhost'
PORT = 12345


class MultiThreadClient(threading.Thread):
    def __init__(self, client_idx):
        super().__init__()
        self.client_idx = client_idx
        self.socket = None

    def run(self):
        try:
            self.socket = socket.socket()
            self.socket.connect((HOST, PORT))
        except socket.error as e:
            print('Oops! Something wrong when connecting to server')
            print(str(e))
            return

        # greeting
        data = self.socket.recv(1024).decode()
        print(f'> Data from server: {data}')

        self.send_and_recv_msg(f'Hello server, I am client #{self.client_idx}')

        # user message
        msg = ''
        while msg.strip().lower() != 'bye':
            msg = input('Input message to server: ')
            self.send_and_recv_msg(msg)

        self.socket.close()

    def send_and_recv_msg(self, msg):
        self.socket.send(str.encode(msg))
        res = self.socket.recv(1024).decode()
        print(f'> Data from server: {res}')


if __name__ == '__main__':
    client_num = input('Please input number of clients needed (default=5): ')
    try:
        client_num = int(client_num)
    except ValueError:
        client_num = 5

    for i in range(1, client_num + 1):
        client = MultiThreadClient(i)
        client.start()
