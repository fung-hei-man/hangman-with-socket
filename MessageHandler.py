import socket

from RoomPool import room_pool


def send_msg(conn, data):
    try:
        conn.send(str.encode(data))
    except socket.error:
        addr = conn.getpeername()
        conn.close()
        room_pool.handle_offline_player(addr)
        raise RuntimeError(f'{addr} has gone offline!!!')


def receive_msg(conn):
    data = conn.recv(1024)
    if not data:
        addr = conn.getpeername()
        conn.close()
        room_pool.handle_offline_player(addr)
        raise RuntimeError(f'{addr} has gone offline!!!')
    else:
        return data.decode()
