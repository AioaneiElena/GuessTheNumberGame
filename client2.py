import socket

def client2():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 1234))

    while True:
        data = client.recv(1024).decode()
        print(data)
        if "choose a number" in data:
            number = input("Enter a number for the other player to guess (between 0 and 50): \n")
            client.sendall(number.encode())
        elif "Goodbye" in data:
            break

    client.close()

if __name__ == "__main__":
    client2()
