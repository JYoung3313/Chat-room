import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = "192.168.1.101"          # same IP as Server
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


# The GUI
root = tk.Tk()
root.title("Chat Room")

chat_box = scrolledtext.ScrolledText(root, state="disabled", width=50, height=15)
chat_box.pack(pady=10)

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT, padx=5)


def receive_messages():
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            if not msg:
                break
            chat_box.config(state="normal")
            chat_box.insert(tk.END, msg + "\n")
            chat_box.config(state="disabled")
            chat_box.see(tk.END)  # Auto scroll to bottom
        except:
            break


def send_message():
    msg = entry.get()
    entry.delete(0, tk.END)
    if msg.strip() != "":
        # Show it in your own chat box
        chat_box.config(state="normal")
        chat_box.insert(tk.END, "You: " + msg + "\n")
        chat_box.config(state="disabled")
        chat_box.see(tk.END)
        
        # Send to server
        client.send(msg.encode("utf-8"))


send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT)


# Start receiving thread
threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()