import time

import MessageHandler

HANGMAN_FIGURE = [
  '''
      +---+
      |   |
          |
          |
          |
          |
    =========
  ''',
  '''
      +---+
      |   |
      O   |
          |
          |
          |
    =========
  ''',
  '''
    +---+
      |   |
      O   |
      |   |
          |
          |
    =========
  ''',
  '''
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
  ''',
  '''
      +---+
      |   |
      O   |
     /|\  |
          |
          |
    =========
  ''',
  '''
      +---+
      |   |
      O   |
     /|\  |
     /    |
          |
    =========
  ''',
  '''
      +---+
      |   |
      O   |
     /|\  |
     / \  |
          |
    =========
  ''',
]


class Player:
    def __init__(self, rm_num, role, conn, addr):
        self.rm_num = rm_num
        self.role = role
        self.conn = conn
        self.addr = addr
        self.room = None

    def assign_room(self, room):
        self.room = room

    def send_welcome_msg(self):
        MessageHandler.send_msg(self.conn, self.addr, f'You are in room #{self.rm_num}! You are the {self.role} in this round!')
        MessageHandler.send_msg(self.conn, self.addr, f'There are {len(self.room.word)} letters in the word')

    def guess_letter(self):
        MessageHandler.send_msg(self.conn, self.addr, 'It\'s your turn! Guess a letter?')
        return MessageHandler.receive_msg(self.conn, self.addr).lower()

    def guess_letter_again(self, letter):
        MessageHandler.send_msg(self.conn, self.addr, f'{letter} used already! Guess another letter?')
        return MessageHandler.receive_msg(self.conn, self.addr).lower()

    def send_guess_result(self, strokes, msg, word_hint):
        figure = HANGMAN_FIGURE[strokes]
        MessageHandler.send_msg(self.conn, self.addr, f'{msg}{figure}\n{word_hint}')
        time.sleep(0.1)

    def send_game_result(self, msg):
        MessageHandler.send_msg(self.conn, self.addr, msg)

    def __repr__(self):
        return f'{self.addr[1]} in room {self.rm_num} as {self.role}'
