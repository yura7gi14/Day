import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(message.strip())
        except:
            break

def main():
    username = input("Username: ")
    password = input("Password: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 12345))

    # 1. 認証送信
    login_msg = f"LOGIN {username} {password}"
    sock.sendall(login_msg.encode())

    response = sock.recv(1024).decode().strip()
    if response != "OK":
        print("Login failed.")
        sock.close()
        return

    print("Login successful. You can now chat.")
    thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
    thread.start()

    while True:
        msg = input()
        if msg.lower() == "exit":
            break
        sock.sendall(msg.encode())

    sock.close()

if __name__ == "__main__":
    main()
