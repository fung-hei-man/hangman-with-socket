import socket
import threading

HOST = 'localhost'
PORT = 12345


class MultiThreadClient(threading.Thread):
    def __init__(self, client_idx):
        super().__init__()
        self.client_idx = client_idx

    def run(self):
        try:
            s = socket.socket()
            s.connect((HOST, PORT))
        except socket.error as e:
            print('Oops! Something wrong when connecting to server')
            print(str(e))
            return

        data = s.recv(1024).decode()
        print(f'> Date from server: {data}')

        s.send(str.encode(f'Hello server, I am client #{self.client_idx}'))
        data = s.recv(1024).decode()
        print(f'> Date from server: {data}')

        s.close()


if __name__ == '__main__':
    client_num = input('Please input number of clients needed (default=5): ')
    try:
        client_num = int(client_num)
    except ValueError:
        client_num = 5

    for i in range(1, client_num+1):
        client = MultiThreadClient(i)
        client.start()
