import logging
import random
import socket
from _thread import start_new_thread

import MessageHandler
from Player import Player
from RoomPool import room_pool

logging.basicConfig(level=logging.DEBUG)


class HangmanConcurrentServer:
    def __init__(self):
        self._roles = ['killer', 'defender']
        self._port = 12345
        self._queue_size = 5
        self._socket = None

    def start_concurrent_server(self):
        try:
            self._socket = socket.socket()
            self._socket.bind(('localhost', self._port))
            self._socket.listen(self._queue_size)
        except socket.error as e:
            print('Oops! Something is wrong when try listening from socket')
            print(str(e))
            return

        print(f'Concurrent server listening to self_port {self._port} with queue size {self._queue_size}')

        while True:
            conn, addr = self._socket.accept()
            start_new_thread(self.arrange_room, (conn, addr))

    def arrange_room(self, conn, addr):
        logging.info(f'Accepted connection from {addr}')

        MessageHandler.send_msg(conn, 'Hello, Welcome to the Hangman game! Do you have a room number?')
        room_num = MessageHandler.receive_msg(conn)
        room_num = None if room_num == ' ' else room_num

        client_msg = ''

        # room num provided
        if room_num is not None:
            logging.debug(f'Client wants to enter room #{room_num}')
            # provided room has two players already
            if room_num in room_pool.rooms:
                client_msg += f'Room #{room_num} is occupied! Create a new room for you :) \n'
                room_num = None  # the number is invalid

            else:
                pending_player = room_pool.find_pending_player(room_num)
                if pending_player is not None:
                    logging.debug(f'Room #{room_num} have 2 players, start it now')
                    if pending_player.rm_num == room_num:
                        client_msg += 'Found your partner!'
                    else:
                        client_msg += f'Room #{room_num} does not exist, but we\'ve got your another player to player with!'
                    self.create_room(client_msg, pending_player, conn, addr)
                    return

        # no room num provided, or is invalid, find a pending player
        pending_player = room_pool.find_pending_player(None)

        if pending_player is None:
            room_num = room_num if room_num is not None else str(random.randint(0, 9999)).rjust(4, '0')
            client_msg += f'Waiting for another player to join... Tell your friend to join with room number #{room_num}!'
            MessageHandler.send_msg(conn, client_msg)

            room_pool.create_pending_player(room_num, random.choice(self._roles), conn, addr)
        else:
            client_msg += 'We\'ve matched a player for you!'
            self.create_room(client_msg, pending_player, conn, addr)

    def create_room(self, msg, pending_player, conn, addr):
        MessageHandler.send_msg(conn, msg)
        new_player = Player(pending_player.rm_num, self._roles[0] if pending_player.role == self._roles[1] else self._roles[1], conn, addr)
        room_pool.create_and_start_room(pending_player.rm_num, pending_player, new_player)


if __name__ == '__main__':
    server = HangmanConcurrentServer()
    server.start_concurrent_server()
