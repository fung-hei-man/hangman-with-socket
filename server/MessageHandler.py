import logging
import socket

from RoomPool import room_pool


def send_msg(conn, addr, data):
    try:
        conn.send(str.encode(data))
    except socket.error:
        room_pool.handle_offline_player(addr)
        conn.close()
        raise RuntimeError(f'{addr} has gone offline!!!')


def receive_msg(conn, addr):
    try:
        logging.debug(f'Expecting response from {conn.getpeername()}')
        data = conn.recv(1024)
        if not data:
            room_pool.handle_offline_player(addr)
            conn.close()
            raise RuntimeError(f'{addr} has gone offline!!!')
        else:
            return data.decode()
    except socket.error:
        room_pool.handle_offline_player(addr)
        conn.close()
        raise RuntimeError(f'{addr} has gone offline!!!')
