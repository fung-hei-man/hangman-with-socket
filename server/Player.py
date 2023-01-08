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
        MessageHandler.send_msg(self.conn, f'You are in room #{self.rm_num}! You are the {self.role} in this round!')
        MessageHandler.send_msg(self.conn, f'There are {len(self.room.word)} letters in the word')

    def guess_letter(self):
        MessageHandler.send_msg(self.conn, 'It\'s your turn! Guess a letter?')
        return MessageHandler.receive_msg(self.conn).lower()

    def guess_letter_again(self, letter):
        MessageHandler.send_msg(self.conn, f'{letter} used already! Guess another letter?')
        return MessageHandler.receive_msg(self.conn).lower()

    def send_guess_result(self, strokes, msg, word_hint):
        figure = HANGMAN_FIGURE[strokes]
        MessageHandler.send_msg(self.conn, f'{msg}{figure}\n{word_hint}')

    def send_game_result(self, msg):
        MessageHandler.send_msg(self.conn, msg)

    def __repr__(self):
        return f'{self.addr[1]} in room {self.rm_num} as {self.role}'
