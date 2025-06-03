import tkinter as tk
from tkinter import ttk
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("400x380")
        self.root.resizable(False, False)

        self.difficulty = tk.StringVar(value="Medium")
        self.number_to_guess = None
        self.attempts = 0

        self.setup_ui()
        self.set_difficulty()  # Initialize game

    def setup_ui(self):
        ttk.Label(self.root, text="🎯 Guess a number!", font=("Arial", 14)).pack(pady=10)

        # Difficulty selection
        ttk.Label(self.root, text="Select Difficulty:", font=("Arial", 10)).pack()
        difficulty_frame = ttk.Frame(self.root)
        difficulty_frame.pack(pady=5)

        for level in ["Easy", "Medium", "Hard"]:
            ttk.Radiobutton(
                difficulty_frame,
                text=level,
                variable=self.difficulty,
                value=level,
                command=self.set_difficulty
            ).pack(side=tk.LEFT, padx=10)

        # Entry for guess
        self.entry = ttk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.check_guess)

        # Submit button
        self.submit_btn = ttk.Button(self.root, text="Submit Guess", command=self.check_guess)
        self.submit_btn.pack(pady=5)

        # Result label
        self.result_label = ttk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        # Attempts
        self.attempt_label = ttk.Label(self.root, text="Attempts: 0", font=("Arial", 10))
        self.attempt_label.pack(pady=5)

        # Restart button
        self.restart_btn = ttk.Button(self.root, text="Restart Game", command=self.restart_game)
        self.restart_btn.pack(pady=10)

    def set_difficulty(self):
        level = self.difficulty.get()
        if level == "Easy":
            self.range_max = 50
        elif level == "Medium":
            self.range_max = 100
        else:
            self.range_max = 500

        self.number_to_guess = random.randint(1, self.range_max)
        self.attempts = 0
        self.attempt_label.config(text="Attempts: 0")
        self.result_label.config(text=f"(Guess a number from 1 to {self.range_max})")
        self.entry.delete(0, tk.END)

    def check_guess(self, event=None):
        guess = self.entry.get()
        self.entry.delete(0, tk.END)

        if not guess.isdigit():
            self.result_label.config(text="❌ Please enter a valid number.")
            return

        guess = int(guess)
        self.attempts += 1
        self.attempt_label.config(text=f"Attempts: {self.attempts}")

        if guess < self.number_to_guess:
            self.result_label.config(text="Too low. Try again.")
        elif guess > self.number_to_guess:
            self.result_label.config(text="Too high. Try again.")
        else:
            self.result_label.config(text=f"🎉 Correct! It was {self.number_to_guess}.")

    def restart_game(self):
        self.set_difficulty()

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()
