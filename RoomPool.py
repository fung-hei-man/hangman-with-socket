import logging
import queue

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

    def create_room(self, rm_num, player1, player2):
        new_room = Room(player1 if player1.role == 'defender' else player2, player1 if player1.role == 'killer' else player2)
        self.rooms.update({rm_num: new_room})

        logging.debug(f'current rooms:\n{self.rooms}')

    def start_room(self, rm_num):
        room = self.rooms.get(rm_num)
        print(room)
        word = room.fetch_word()
        logging.info(f'Room {rm_num} decided word ""{word}""')

        room.defender.start()
        room.killer.start()


room_pool = RoomPool()