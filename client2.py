import socket

def client2():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555))

    while True:
        try:
            data = client.recv(1024).decode()
            print(data)

            if "choose a number" in data:
                while True:
                    number = input("Enter a number for the other player to guess (between 0 and 50): ").strip()
                    if number.isdigit() and 0 <= int(number) <= 50:
                        client.sendall(number.encode())
                        break
                    else:
                        print("Invalid input. Please enter a valid number.")

            elif "Goodbye" in data:
                break
        except Exception as e:
            print(f"Eroare : {e}")
            break

    client.close()

if __name__ == "__main__":
    client2()
