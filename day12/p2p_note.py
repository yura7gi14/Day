import socket
import threading
import tkinter as tk
import argparse
import time

class P2PNoteApp:
    def __init__(self, master, conn):
        self.master = master
        self.conn = conn
        self.text = tk.Text(master, wrap="word", font=("Arial", 12))
        self.text.pack(expand=True, fill="both")
        self.last_content = ""

        threading.Thread(target=self.receive_loop, daemon=True).start()
        self.sync_loop()

    def sync_loop(self):
        current = self.text.get("1.0", "end-1c")
        if current != self.last_content:
            try:
                self.conn.sendall(current.encode("utf-8"))
                self.last_content = current
            except:
                pass
        self.master.after(1000, self.sync_loop)  # 毎秒同期

    def receive_loop(self):
        while True:
            try:
                data = self.conn.recv(65536).decode("utf-8")
                if not data:
                    break
                self.text.delete("1.0", "end")
                self.text.insert("1.0", data)
                self.last_content = data
            except:
                break

def start_host(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(1)
    print(f"[ホスト待機中] ポート {port} で接続を待っています...")
    conn, addr = server.accept()
    print(f"[接続成功] {addr} と接続しました。")
    return conn

def connect_to_peer(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f"[接続成功] {host}:{port}")
    return sock

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P2P同期ノート")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--host", action="store_true", help="ホストとして起動")
    group.add_argument("--connect", metavar="IP", help="相手のIPに接続")
    parser.add_argument("--port", type=int, default=12345, help="ポート番号 (default: 12345)")
    args = parser.parse_args()

    if args.host:
        conn = start_host(args.port)
    else:
        conn = connect_to_peer(args.connect, args.port)

    root = tk.Tk()
    root.title("P2P同期ノート")
    app = P2PNoteApp(root, conn)
    root.mainloop()
