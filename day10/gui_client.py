import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")  # ← 英語タイトルで文字化け回避

        self.text_area = tk.Text(master, state="disabled", height=20, width=50, font=("Meiryo", 12))
        self.text_area.pack(padx=10, pady=5)

        self.entry = tk.Entry(master, width=40, font=("Meiryo", 12))
        self.entry.pack(side="left", padx=(10, 0), pady=(0, 10))
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(side="right", padx=(0, 10), pady=(0, 10))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = ""
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.sock.connect(("127.0.0.1", 12345))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Cannot connect to server: {e}")
            self.master.destroy()
            return

        self.username = simpledialog.askstring("Login", "Username:")
        password = simpledialog.askstring("Login", "Password:", show='*')
        if not self.username or not password:
            messagebox.showerror("Login Failed", "Username and password are required.")
            self.master.destroy()
            return

        login_msg = f"LOGIN {self.username} {password}"
        self.sock.sendall(login_msg.encode("utf-8"))

        response = self.sock.recv(1024).decode("utf-8", errors="replace").strip()
        if response != "OK":
            messagebox.showerror("Login Failed", "Invalid username or password.")
            self.master.destroy()
            return

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        msg = self.entry.get()
        if msg:
            try:
                self.sock.sendall(msg.encode("utf-8"))
                self.entry.delete(0, tk.END)
            except:
                messagebox.showerror("Send Error", "Failed to send message.")
                self.master.destroy()

    def receive_messages(self):
        while True:
            try:
                message = self.sock.recv(1024).decode("utf-8", errors="replace")
                if not message:
                    break
                self.display_message(message)
            except:
                break

    def display_message(self, message):
        self.text_area.config(state="normal")
        self.text_area.insert("end", message + "\n")
        self.text_area.yview("end")
        self.text_area.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
