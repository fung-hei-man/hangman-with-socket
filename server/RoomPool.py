import logging
import socket
import time

from Player import Player
from Room import Room


class RoomPool:
    def __init__(self):
        self.rooms = {}
        self.pending_players = []

    def find_pending_player(self, room_num):
        target_idx = None
        if room_num is not None:
            for idx, player in enumerate(self.pending_players):
                if player.rm_num == room_num:
                    target_idx = idx

            if target_idx is not None:
                return self.pending_players.pop(target_idx)

        return None if len(self.pending_players) == 0 else self.pending_players.pop()

    def create_pending_player(self, room_num, role, conn, addr):
        player = Player(room_num, role, conn, addr)
        self.pending_players.insert(0, player)  # insert in the beginning

    def create_and_start_room(self, rm_num, player1, player2):
        new_room = Room(rm_num, player1 if player1.role == 'defender' else player2, player1 if player1.role == 'killer' else player2)
        self.rooms.update({rm_num: new_room})
        logging.debug(f'current rooms:\n{self.rooms}')

        word = new_room.fetch_word()
        logging.info(f'[Room #{rm_num}] Decided word ""{word}""')

        new_room.defender.assign_room(new_room)
        new_room.killer.assign_room(new_room)

        new_room.defender.send_welcome_msg()
        new_room.killer.send_welcome_msg()

        time.sleep(0.1)
        new_room.start()

    def recreate_room(self, rm_num, player1, player2):
        # delete and create room again
        self.rooms.pop(rm_num)
        self.create_and_start_room(rm_num, player1, player2)

    def handle_offline_player(self, raddr):
        logging.debug(f'Handle {raddr} disconnect')
        target_idx = None
        for idx, player in enumerate(self.pending_players):
            if player.addr == raddr:
                logging.debug(f'Find player {raddr} in pending list')
                target_idx = idx
        if target_idx is not None:
            self.pending_players.pop(target_idx)
        logging.debug(f'Pending players num: {len(self.pending_players)}')

        for rm_num, room in self.rooms.items():
            if room.killer.addr == raddr or room.defender.addr == raddr:
                target_idx = rm_num

                logging.debug(f'Find player {raddr} in room {rm_num}')
                msg = 'Your partner gone offline. Game ended :('
                try:
                    room.killer.conn.send(str.encode(msg))
                    room.killer.conn.close()
                    room.defender.conn.send(str.encode(msg))
                    room.defender.conn.close()
                except socket.error:
                    logging.error('Fail to send msg when handling disconnect (probably normal)')

        self.rooms.pop(target_idx)
        logging.debug(f'current rooms:\n{self.rooms}')


room_pool = RoomPool()
