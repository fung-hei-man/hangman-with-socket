import logging
import random
import threading
import time

import RoomPool


class Room(threading.Thread):
    def __init__(self, rm_num, defender, killer):
        threading.Thread.__init__(self)
        self.rm_num = rm_num
        self.defender = defender
        self.killer = killer
        self.current_player = self.killer
        self.strokes = 0

        self.word = None
        self.word_letters = None
        self.guessed_letters = set()
        self.correct_letters = set()

    def fetch_word(self):
        with open('words.txt', 'r') as file:
            f = file.readlines()

            while self.word is None or len(self.word) < 10:
                i = random.randrange(0, len(f) - 1)

                self.word = f[i][:-1].lower()
                self.word_letters = set(self.word)

        return self.word

    def run(self):
        while self.strokes < 6 and len(self.word_letters) != len(self.correct_letters):
            logging.debug(f'[Room #{self.rm_num}] {self.current_player.role} turn to guess')
            player_guess = self.current_player.guess_letter()
            # avoid guessing same letter
            while player_guess in self.guessed_letters:
                player_guess = self.current_player.guess_letter_again(player_guess)
            self.guessed_letters.add(player_guess)

            # correct = continue guessing, killer correct = add stroke
            # wrong = switch
            if player_guess in self.word_letters:
                logging.debug(f'[Room #{self.rm_num}] {self.current_player.role} guess "{player_guess}", correct')

                self.correct_letters.add(player_guess)

                if 'killer' == self.current_player.role:
                    self.strokes += 1
                    killer_msg = 'You get it right! A stroke is added to the hangman figure!'
                    defender_msg = f'Killer guessed "{player_guess}" and it is correct! A stroke is added to the hangman figure!'
                else:
                    killer_msg = f'Defender guessed "{player_guess}" and it is correct!'
                    defender_msg = 'You get it right!'

            else:
                logging.debug(f'[Room #{self.rm_num}] {self.current_player.role} guess "{player_guess}", wrong')

                if 'killer' == self.current_player.role:
                    killer_msg = 'You get it wrong :( It\'s defender\'s turn!'
                    defender_msg = f'Killer guessed "{player_guess}" and it is wrong!'
                else:
                    killer_msg = f'Defender guessed "{player_guess}" and it is wrong!'
                    defender_msg = 'You get it wrong :( It\'s killer\'s turn!'
                # switch
                self.current_player = self.defender if self.current_player.role == 'killer' else self.killer

            display_word = [letter if letter in self.correct_letters else '_' for letter in self.word]
            self.killer.send_guess_result(self.strokes, killer_msg, display_word)
            self.defender.send_guess_result(self.strokes, defender_msg, display_word)

        self.handle_end_game()
        time.sleep(0.3)
        self.switch_role_restart_game()

    def handle_end_game(self):
        winner_msg = f'YOU ARE THE WINNER!!! The word is ""{self.word}"".'
        loser_msg = f'You lose the game :( The word is ""{self.word}"".'
        draw_msg = 'Draw!'

        # Word complete + Figure not complete => Defender wins
        # Word not complete + Figure complete => Killer wins
        # Word complete + Figure complete => draw
        if self.strokes == 6 and len(self.word_letters) == len(self.correct_letters):
            self.killer.send_game_result(draw_msg)
            self.defender.send_game_result(draw_msg)

        elif self.strokes == 6:
            self.killer.send_game_result(winner_msg + ' Poor man dead!')
            self.defender.send_game_result('Killer killed the poor man!! ' + loser_msg)

        elif len(self.word_letters) == len(self.correct_letters):
            self.killer.send_game_result('Defender saved the poor man!! ' + loser_msg)
            self.defender.send_game_result(winner_msg + ' You save the man!')

        time.sleep(0.1)
        self.killer.send_game_result("=================================================")
        self.defender.send_game_result("=================================================")

    def switch_role_restart_game(self):
        self.killer.role = 'defender'
        self.defender.role = 'killer'
        RoomPool.room_pool.recreate_room(self.rm_num, self.defender, self.killer)

    def __repr__(self):
        return f'player1: {self.defender}, player2: {self.killer}, word: {self.word} \n'
