import socket
import threading
import time
import random

clients = []
number_to_guess = None
max_score = float('inf')
scores = []

def handle_client_vs_server(conn):
    """Client vs Server: Serverul generează un număr și clientul încearcă să îl ghicească."""
    global number_to_guess, scores, max_score

    number_to_guess = random.randint(0, 50)
    attempts = 0
    conn.sendall("The server has generated a number between 0 and 50. Start guessing!\n".encode())

    while True:
        guess = conn.recv(1024).decode().strip()
        if guess.lower() == 'quit':
            conn.sendall("You chose to quit the game. Goodbye!\n".encode())
            conn.close()
            return

        try:
            guess = int(guess)
            attempts += 1
            if guess == number_to_guess:
                conn.sendall(f"Correct! You guessed the number in {attempts} attempts.\n".encode())
                scores.append(attempts)
                max_score = min(scores)
                conn.sendall(f"Game Over! Your Score: {attempts}, Best Score: {max_score}\n".encode())
                break
            elif guess < number_to_guess:
                conn.sendall("The number is higher. Try again!\n".encode())
            else:
                conn.sendall("The number is lower. Try again!\n".encode())
        except ValueError:
            conn.sendall("Invalid input. Please enter a number between 0 and 50.\n".encode())

    conn.sendall("Do you want to play again? (yes/quit): ".encode())
    response = conn.recv(1024).decode().strip().lower()
    if response == 'quit':
        conn.sendall("Goodbye!\n".encode())
        conn.close()
    else:
        handle_client_vs_server(conn)  # Restart game


def handle_client_vs_client(conn, client_id):
    """Client vs Client: Client 2 alege numărul, Client 1 încearcă să-l ghicească."""
    global number_to_guess, clients, max_score, scores

    if client_id == 2:
        # Client 2 alege numărul
        conn.sendall("You are Client 2. Choose a number for the other player to guess (0-50):\n".encode())
        while True:
            try:
                data = conn.recv(1024).decode().strip()  # Așteaptă input de la Client 2
                number_to_guess = int(data)
                if 0 <= number_to_guess <= 50:
                    print(f"[INFO] Client 2 chose the number: {number_to_guess}")
                    conn.sendall("The number has been sent to the other player.\n".encode())
                    clients[0][0].sendall("The other player has chosen a number. Start guessing!\n".encode())
                    break
                else:
                    conn.sendall("Invalid number. Please choose a number between 0 and 50:\n".encode())
            except ValueError:
                conn.sendall("Invalid input. Please enter a valid number:\n".encode())
    elif client_id == 1:
        # Client 1 ghicește
        attempts = 0
        conn.sendall("Waiting for the other player to choose a number...\n".encode())

        while number_to_guess is None:
            time.sleep(1)  # Așteaptă să fie setat numărul de către Client 2

        while True:
            conn.sendall("Enter your guess (or type 'quit' to exit): ".encode())
            guess = conn.recv(1024).decode().strip()

            if guess.lower() == 'quit':
                conn.sendall("You quit the game. Goodbye!\n".encode())
                clients[1][0].sendall("The other player quit the game. Goodbye!\n".encode())
                close_all_connections()
                return

            try:
                guess = int(guess)
                attempts += 1

                if guess == number_to_guess:
                    conn.sendall(f"Correct! You guessed the number in {attempts} attempts.\n".encode())
                    scores.append(attempts)
                    max_score = min(scores)
                    for c in clients:
                        c[0].sendall(f"Game Over! The number was {number_to_guess}. Attempts: {attempts}, Best Score: {max_score}\n".encode())
                    return
                elif guess < number_to_guess:
                    conn.sendall("The number is higher. Try again!\n".encode())
                else:
                    conn.sendall("The number is lower. Try again!\n".encode())
            except ValueError:
                conn.sendall("Invalid input. Please enter a valid number.\n".encode())

def close_all_connections():
    """Închide conexiunile pentru toți clienții și oprește serverul."""
    for c in clients:
        try:
            c[0].close()
        except Exception as e:
            print(f"[ERROR] Error closing connection: {e}")
    print("[INFO] All connections closed. Server shutting down.")

def start_server():
    global clients

    print("Choose game mode:\n1. Client vs Server\n2. Client vs Client")
    mode = input("Enter 1 or 2: ").strip()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5555))
    server.listen(2)
    print("[INFO] Server is listening on port 5555...")

    if mode == '1':
        print("[INFO] Starting Client vs Server mode.")
        conn, addr = server.accept()
        handle_client_vs_server(conn)
    elif mode == '2':
        print("[INFO] Starting Client vs Client mode.")
        while len(clients) < 2:
            conn, addr = server.accept()
            clients.append((conn, addr))
            client_id = len(clients)
            thread = threading.Thread(target=handle_client_vs_client, args=(conn, client_id))
            thread.start()
    else:
        print("[ERROR] Invalid mode selected. Restart the server.")

if __name__ == "__main__":
    start_server()
