import logging
import random
import re
import socket
from _thread import *

from Player import Player
from RoomPool import room_pool

PORT = 12345
QUEUE_SIZE = 5
ROLES = ['killer', 'defender']

logging.basicConfig(level=logging.DEBUG)


def start_concurrent_server():
    try:
        s = socket.socket()
        s.bind(('localhost', PORT))
        s.listen(QUEUE_SIZE)
    except socket.error as e:
        print('Oops! Something is wrong when try listening from socket')
        print(str(e))
        return

    print(f'Concurrent server listening to port {PORT} with queue size {QUEUE_SIZE}')

    while True:
        conn, addr = s.accept()
        start_new_thread(arrange_room, (conn, addr))


def arrange_room(conn, addr):
    logging.info(f'Accepted connection from {addr}')

    conn.send(str.encode('Hello, Welcome to the Hangman game! Do you have a room number?'))
    room_num = conn.recv(1024).decode()
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
                conn.send(str.encode(client_msg))

                room_num = pending_player.rm_num
                new_player = Player(room_num, ROLES[0] if pending_player.role == ROLES[1] else ROLES[1], conn, addr)
                room_pool.create_room(pending_player.rm_num, pending_player, new_player)
                room_pool.start_room(pending_player.rm_num)
                return

    # no room num provided, or is invalid, find a pending player
    pending_player = room_pool.find_pending_player(None)

    if pending_player is None:
        room_num = room_num if room_num is not None else str(random.randint(0, 9999)).rjust(4, '0')
        client_msg += f'Waiting for another player to join... Tell your friend to join with room number #{room_num}!'
        conn.send(str.encode(client_msg))

        room_pool.create_pending_player(room_num, random.choice(ROLES), conn, addr)
    else:
        client_msg += 'We\'ve matched a player for you!'
        conn.send(str.encode(client_msg))

        new_player = Player(pending_player.rm_num, ROLES[0] if pending_player.role == ROLES[1] else ROLES[1], conn, addr)
        room_pool.create_room(pending_player.rm_num, pending_player, new_player)
        room_pool.start_room(pending_player.rm_num)


def serve_client(conn, addr):
    client_idx = None

    with conn:
        conn.send(str.encode('Hello! You are now connected to the concurrent sever'))

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
    start_concurrent_server()
