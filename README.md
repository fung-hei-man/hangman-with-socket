# Socket Programming - Hangman

## Modified Hangman
- Two player roles, Killer and Defender. Killer always goes first.
- Players can start a new game or join one with a game ID. Roles are assigned randomly.
- Player who guesses a letter correctly can continue guessing, passes to another player otherwise
- Stroke is added to the hangman if Killer makes a correct guess
- Winning condition:
  - Hangman figure completed before word completed => Killer wins
  - Word completed before hangman figure completed => Defender wins
  - Both completed at the same round => Draw

## Concurrent Server
> Port: 12345

This server uses threads to serve connection requests. Client should be able to connect to server immediately regardless of number of connected clients.

```
cd server
python HangmanConcurrentServer.py
```
\* `MultiThreadClient.py` cannot display the input prompt for different clients at the same time

## Single Thread Client
```
cd client
python SingleClient.py
```