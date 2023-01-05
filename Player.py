import threading

import MessageHandler


class Player(threading.Thread):
    def __init__(self, rm_num, role, conn, addr):
        threading.Thread.__init__(self)
        self.rm_num = rm_num
        self.role = role
        self.conn = conn
        self.addr = addr

    def send_welcome_msg(self):
        MessageHandler.send_msg(self.conn, f'You are in room #{self.rm_num}! You are the {self.role} in this round!')

    def run(self):
        self.send_welcome_msg()

    def __repr__(self):
        return f'{self.addr[1]} in room {self.rm_num} as {self.role}'
