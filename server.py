import socket
import threading
import random
import time

clients = []
number_to_guess = None
max_score = float('inf')
scores = []

def handle_client_vs_client(conn, addr, client_id):
    global number_to_guess, max_score, clients, scores
    print(f"Client {client_id} connected: {addr}")
    conn.sendall(f"Welcome, Client {client_id}!\n".encode())

    while True:
        if client_id == 1:
            conn.sendall("Waiting to see if another client connects...\n".encode())
            while len(clients) < 2:
                time.sleep(1)
            conn.sendall("Another client has connected. They will choose a number for you to guess.\n".encode())

        elif client_id == 2:
            conn.sendall("You can choose a number for the other player to guess".encode())
            while True:
                try:
                    number_to_guess = int(conn.recv(1024).decode().strip())
                    if 0 <= number_to_guess <= 50:
                        break
                    else:
                        conn.sendall("Invalid input. Please enter a number between 0 and 50:\n".encode())
                except ValueError:
                    conn.sendall("Invalid input. Please enter a valid integer:\n".encode())

            clients[0][0].sendall("The other client has chosen a number. Start guessing!\n".encode())

        if client_id == 1:
            attempts = 0
            while True:
                try:
                    guess = conn.recv(1024).decode().strip()
                    if guess.lower() == 'quit':
                        conn.sendall("You chose to quit the game. Goodbye!\n".encode())
                        clients[1][0].sendall("The other player quit the game. Goodbye!\n".encode())
                        close_all_connections()
                        return

                    guess = int(guess)
                    attempts += 1

                    if guess == number_to_guess:
                        conn.sendall(f"Correct! You guessed the number in {attempts} attempts.\n".encode())
                        scores.append(attempts)
                        max_score = min(scores)
                        break
                    elif guess < number_to_guess:
                        conn.sendall("The number is higher. Try again!\n".encode())
                    else:
                        conn.sendall("The number is lower. Try again!\n".encode())

                except ValueError:
                    conn.sendall("Invalid input. Please enter a valid integer:\n".encode())

            for c in clients:
                c[0].sendall(f"Game Over! The number was {number_to_guess}. Final Score: {attempts}, Max Score: {max_score}\n".encode())

            conn.sendall("Do you want to play again? ".encode())
            response = conn.recv(1024).decode().strip().lower()
            if response == 'quit':
                conn.sendall("You chose to quit the game. Goodbye!\n".encode())
                clients[1][0].sendall("The other player quit the game. Goodbye!\n".encode())
                close_all_connections()
                return
            else:
                clients[1][0].sendall("Please choose a new number for the next round (between 0 and 50):\n".encode())

def handle_client_vs_server(conn, addr):
    print(f"Client connected: {addr}")
    conn.sendall("Welcome to the Guess the Number game!\n".encode())

    while True:
        number_to_guess = random.randint(0, 50)
        print(f"Chosen number: {number_to_guess}")
        conn.sendall("I have chosen a number between 0 and 50. Start guessing!\n".encode())
        attempts = 0

        while True:
            try:
                guess = conn.recv(1024).decode().strip()
                if guess.lower() == 'quit':
                    conn.sendall("You chose to quit the game. Goodbye!\n".encode())
                    return

                guess = int(guess)
                attempts += 1

                if guess == number_to_guess:
                    conn.sendall(f"Correct! You guessed the number in {attempts} attempts.\n".encode())
                    break
                elif guess < number_to_guess:
                    conn.sendall("The number is higher. Try again!\n".encode())
                else:
                    conn.sendall("The number is lower. Try again!\n".encode())

            except ValueError:
                conn.sendall("Invalid input. Please enter a valid integer:\n".encode())

        conn.sendall("Do you want to play again? (yes/quit): ".encode())
        response = conn.recv(1024).decode().strip().lower()
        if response == 'quit':
            conn.sendall("Goodbye!\n".encode())
            break

def close_all_connections():
    for c in clients:
        try:
            c[0].close()
        except Exception as e:
            print(f"Error closing connection: {e}")

def start_server():
    global clients
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 1234))
    server.listen(2)
    game_type = input("Choose game_type: 1 for Client vs Client, 2 for Client vs Server: ").strip()

    if game_type == '1':
        while len(clients) < 2:
            conn, addr = server.accept()
            clients.append((conn, addr))
            client_id = len(clients)
            thread = threading.Thread(target=handle_client_vs_client, args=(conn, addr, client_id))
            thread.start()
    elif game_type == '2':
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client_vs_server, args=(conn, addr))
            thread.start()
    else:
        print("Invalid game_type. Server shutting down.")

if __name__ == "__main__":
    start_server()
