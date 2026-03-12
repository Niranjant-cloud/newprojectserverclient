import socket
import threading
import tkinter as tk
from tkinter import simpledialog

HOST = "127.0.0.1"
PORT = 4100

# connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# tkinter setup
root = tk.Tk()
root.withdraw()

username = simpledialog.askstring("Username", "Enter your username")

chat_window = tk.Toplevel(root)
chat_window.title("Chat Client")

chat_box = tk.Text(chat_window, height=20, width=50)
chat_box.pack()

msg_entry = tk.Entry(chat_window, width=50)
msg_entry.pack()

def receive():
    while True:
        try:
            message = client.recv(1024).decode()

            if message == "USERNAME":
                client.send(username.encode())
            else:
                chat_box.insert(tk.END, message + "\n")
                chat_box.see(tk.END)

        except:
            chat_box.insert(tk.END, "Connection lost.\n")
            break


def send_message(event=None):
    message = msg_entry.get()

    if message.strip() != "":
        full_message = f"{username}: {message}"
        client.send(full_message.encode())

    msg_entry.delete(0, tk.END)


send_btn = tk.Button(chat_window, text="Send", command=send_message)
send_btn.pack()

# press Enter to send
msg_entry.bind("<Return>", send_message)

# start receive thread
receive_thread = threading.Thread(target=receive)
receive_thread.daemon = True
receive_thread.start()

root.mainloop()