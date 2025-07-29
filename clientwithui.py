import socket
import tkinter as tk
from tkinter import messagebox

class ClientWithUi:
    def __init__(self):
        # Network connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("127.0.0.1", 4337))
        self.sock.send("competitor program'a bağlandı".encode())

        # Main window
        self.root = tk.Tk()
        self.root.title("🎓 Program - Contestant")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e2f")

        # Question label
        self.question_label = tk.Label(
            self.root, text="", wraplength=650, justify="left",
            font=("Segoe UI", 14, "bold"), fg="#f8f8f2", bg="#1e1e2f"
        )
        self.question_label.pack(pady=30)

        # Option buttons (A, B, C, D)
        self.options_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.options_frame.pack()

        self.option_buttons = {}
        for idx, option in enumerate(["A", "B", "C", "D"]):
            btn = tk.Button(
                self.options_frame, text=option + " -", width=25, height=2,
                font=("Segoe UI", 12),
                bg="#282a36", fg="#f8f8f2", activebackground="#44475a",
                command=lambda o=option: self.send_answer(o)
            )
            btn.grid(row=idx//2, column=idx%2, padx=20, pady=10)
            self.option_buttons[option] = btn

        # Lifeline buttons
        self.lifeline_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.lifeline_frame.pack(pady=20)

        self.audience_btn = tk.Button(
            self.lifeline_frame, text="🧑‍🤝‍🧑 Seyirci Jokeri", width=20,
            font=("Segoe UI", 10),
            bg="#50fa7b", fg="black", command=lambda: self.send_answer("S")
        )
        self.audience_btn.grid(row=0, column=0, padx=20)

        self.fifty_btn = tk.Button(
            self.lifeline_frame, text="✂️ Yarı Yarıya Jokeri", width=20,
            font=("Segoe UI", 10),
            bg="#ffb86c", fg="black", command=lambda: self.send_answer("Y")
        )
        self.fifty_btn.grid(row=0, column=1, padx=20)

        # Message and result labels
        self.message_label = tk.Label(
            self.root, text="", fg="#8be9fd",
            bg="#1e1e2f", font=("Segoe UI", 11, "italic")
        )
        self.message_label.pack(pady=5)

        self.result_label = tk.Label(
            self.root, text="", fg="#ff5555",
            bg="#1e1e2f", font=("Segoe UI", 13, "bold")
        )
        self.result_label.pack(pady=10)

        self.receive_question()
        self.root.mainloop()

    def receive_question(self):
        data = self.sock.recv(1024).decode()
        if not data or "Yarışma sona erdi" in data:
            self.question_label.config(text="🏁 Yarışma sona erdi.")
            self.disable_all_buttons()
            return
        self.question_label.config(text=data)
        self.message_label.config(text="")
        self.result_label.config(text="")

    def send_answer(self, answer):
        self.sock.send(answer.encode())

        if answer in ["S", "Y"]:
            lifeline_response = self.sock.recv(1024).decode()
            self.message_label.config(text=lifeline_response)

            # Disable joker button
            if answer == "S":
                self.audience_btn.config(state=tk.DISABLED)
            elif answer == "Y":
                self.fifty_btn.config(state=tk.DISABLED)
            return

        # Get result of answer (Doğru mu yanlış mı vs.)
        result = self.sock.recv(1024).decode()
        self.result_label.config(text=result)

        if "Yarışma sona erdi" in result:
            self.disable_all_buttons()
        else:
            self.receive_question()

    def disable_all_buttons(self):
        for btn in self.option_buttons.values():
            btn.config(state=tk.DISABLED)
        if hasattr(self, 'audience_btn'):
            self.audience_btn.config(state=tk.DISABLED)
        if hasattr(self, 'fifty_btn'):
            self.fifty_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    ClientWithUi()
