import socket
import threading

clients = []
users = {
    "alice": "password123",
    "bob": "secure456",
    "carol": "qwerty789"
}
active_users = {}

def broadcast(message):  # ← source_socket 引数削除
    for client in clients:
        try:
            client.sendall(message.encode("utf-8"))
        except:
            clients.remove(client)


def handle_client(client_socket):
    try:
        login_data = client_socket.recv(1024).decode("utf-8", errors="replace").strip()
        parts = login_data.split()
        if len(parts) != 3 or parts[0] != "LOGIN":
            client_socket.sendall("FAIL\n".encode("utf-8"))
            client_socket.close()
            return

        _, username, password = parts
        if users.get(username) != password:
            client_socket.sendall("FAIL\n".encode("utf-8"))
            client_socket.close()
            return

        client_socket.sendall("OK\n".encode("utf-8"))
        clients.append(client_socket)
        active_users[client_socket] = username
        print(f"[LOGIN SUCCESS] {username}")

        while True:
            msg = client_socket.recv(1024).decode("utf-8", errors="replace")
            if not msg:
                break
            print(f"{username}: {msg}")
            broadcast(f"{username}: {msg}")  # ← source_socket を渡さない


    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        active_users.pop(client_socket, None)
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen()
    print("Server listening on port 12345...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main()
