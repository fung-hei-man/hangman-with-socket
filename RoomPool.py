import logging

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
        new_room = Room(player1 if player1.role == 'defender' else player2, player1 if player1.role == 'killer' else player2)
        self.rooms.update({rm_num: new_room})

        word = new_room.fetch_word()
        logging.info(f'Room {rm_num} decided word ""{word}""')

        new_room.defender.start()
        new_room.killer.start()

        logging.debug(f'current rooms:\n{self.rooms}')

    def handle_offline_player(self, raddr):
        logging.debug(f'Handle {raddr} disconnect')
        target_idx = None
        for idx, player in enumerate(self.pending_players):
            if player.conn.getpeername() == raddr:
                logging.debug(f'Find player {raddr} in pending list')
                target_idx = idx
        if target_idx is not None:
            self.pending_players.pop(target_idx)
        logging.debug(f'Pending players num: {len(self.pending_players)}')

        for rm_num, room in self.rooms.items():
            if room.killer.conn.getpeername() == raddr or room.defender.conn.getpeername() == raddr:
                self.rooms.pop(rm_num)

                logging.debug(f'Find player {raddr} in room {rm_num}')
                msg = 'Your partner gone offline. Game ended :('
                room.killer.conn.send(str.encode(msg))
                room.killer.conn.close()
                room.defender.conn.send(str.encode(msg))
                room.defender.conn.close()

            logging.debug(f'current rooms:\n{self.rooms}')


room_pool = RoomPool()
