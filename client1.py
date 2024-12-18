import socket

def client1():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555))

    while True:
        data = client.recv(1024).decode()
        print(data)

        if "Start guessing" in data or "higher" in data or "lower" in data:
            guess = input("Enter your guess (or type 'quit' to exit): ")
            client.sendall(guess.encode())
            if guess.lower() == 'quit':
                break
        elif "Do you want to play again?" in data:
            response = input("Enter 'yes' to play again or 'quit' to exit: ")
            client.sendall(response.encode())
            if response.lower() == 'quit':
                break
        elif "Goodbye" in data:
            break

    client.close()

if __name__ == "__main__":
    client1()
