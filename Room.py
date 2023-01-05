import random
import threading


class Room(threading.Thread):
    def __init__(self, defender, killer):
        threading.Thread.__init__(self)
        self.defender = defender
        self.killer = killer
        self.word = None

    def fetch_word(self):
        file = open('words.txt')
        f = file.readlines()
        i = random.randrange(0, len(f) - 1)

        self.word = f[i][:-1]
        return self.word

    def __repr__(self):
        return f'player1: {self.defender}, player2: {self.killer}, word: {self.word} \n'
