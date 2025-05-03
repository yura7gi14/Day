import socket
import threading
import argparse

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode("utf-8")
            if not data:
                print("[接続終了]")
                break
            print(f"\n相手: {data}")
        except:
            break

def start_host(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(1)
    print(f"[待機中] ポート {port} で接続を待っています...")

    conn, addr = server.accept()
    print(f"[接続成功] {addr} と接続しました。")

    threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()

    while True:
        msg = input("自分: ")
        if msg.lower() == "exit":
            conn.close()
            break
        conn.sendall(msg.encode("utf-8"))

def connect_to_peer(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        print(f"[接続成功] {host}:{port} に接続しました。")
    except Exception as e:
        print(f"[接続失敗] {e}")
        return

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    while True:
        msg = input("自分: ")
        if msg.lower() == "exit":
            sock.close()
            break
        sock.sendall(msg.encode("utf-8"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P2P Chat - Python")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--host", action="store_true", help="ホストとして起動")
    group.add_argument("--connect", metavar="IP", help="指定IPに接続")

    parser.add_argument("--port", type=int, default=12345, help="使用するポート番号（デフォルト: 12345）")
    args = parser.parse_args()

    if args.host:
        start_host(args.port)
    else:
        connect_to_peer(args.connect, args.port)
