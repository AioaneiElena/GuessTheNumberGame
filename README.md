# 🎯 Guess the Number – Multiplayer Python Game

**Guess the Number** is a console-based multiplayer game developed in Python using socket programming. It features two game modes:

- 👥 **Client vs Client** – One player sets a number, and the other guesses.
- 🤖 **Client vs Server** – The server randomly generates a number, and the player tries to guess it.

---

## 🚀 Features

- Real-time interaction via TCP sockets
- Threaded server supports multiple simultaneous games
- Quit/resume functionality
- Score tracking and feedback per round
- Friendly text-based interface

---

## ⚙️ Tech Stack

- **Python 3**
- `socket` – network communication
- `threading` – concurrent client handling
- Command Line Interface (CLI)

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/username/guess-the-number.git
cd guess-the-number
```
### 2. Start the server
```bash
python server.py
```
You will be prompted to choose the game type:
1 – Client vs Client
2 – Client vs Server

### 3. Launch the clients in separate terminals
For Client vs Client:
```bash
python client1.py   # Guesser
python client2.py   # Number setter
```
For Client vs Server:
```bash
python client1.py   # Connect and play against the server
```
