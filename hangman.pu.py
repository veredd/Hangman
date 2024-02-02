import tkinter as tk
from tkinter import messagebox
import random

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")

        self.difficulty_levels = {
            "easy": (3, 5),
            "medium": (5, 8),
            "hard": (8, 10)
        }

        self.word_list = {
            "easy": ["cat", "dog", "sun", "moon", "rain", "fish"],
            "medium": ["python", "hangman", "apple", "table", "happy", "cloud"],
            "hard": ["programming", "computer", "software", "developer", "coding"]
        }

        self.word_to_guess = ""
        self.guesses_left = 6
        self.guessed_letters = set()
        self.difficulty = tk.StringVar()
        self.difficulty.set("easy")

        self.difficulty_menu = tk.OptionMenu(self.master, self.difficulty, *self.difficulty_levels.keys())
        self.difficulty_menu.pack(pady=10)

        self.info_label = tk.Label(self.master, text="")
        self.info_label.pack(pady=5)

        self.hangman_display = tk.Label(self.master, text="")
        self.hangman_display.pack(pady=10)

        self.word_display = tk.Label(self.master, text="")
        self.word_display.pack(pady=10)

        self.guess_entry = tk.Entry(self.master)
        self.guess_entry.pack(pady=10)

        self.guess_button = tk.Button(self.master, text="Guess", command=self.make_guess)
        self.guess_button.pack(pady=10)

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_game)
        self.reset_button.pack(pady=10)

        self.choose_word()

    def choose_word(self):
        difficulty_range = self.difficulty_levels[self.difficulty.get()]
        self.word_to_guess = random.choice([word for word in self.word_list[self.difficulty.get()] if difficulty_range[0] <= len(word) <= difficulty_range[1]])
        self.guesses_left = 6
        self.guessed_letters = set()
        self.update_display()

        # Display difficulty info
        self.info_label.config(text=f"Difficulty: {self.difficulty.get().capitalize()} | Guesses Left: {self.guesses_left}")

        # Display initial hangman
        self.hangman_display.config(text=self.display_hangman(0))

    def display_word(self):
        return " ".join(letter if letter in self.guessed_letters else "_" for letter in self.word_to_guess)

    def update_display(self):
        self.word_display.config(text=self.display_word())

    def make_guess(self):
        guess = self.guess_entry.get().lower()

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Guess", "Please enter a single alphabetical character.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Duplicate Guess", f"You already guessed '{guess}'.")
            return

        self.guessed_letters.add(guess)

        if guess not in self.word_to_guess:
            self.guesses_left -= 1

            # Update and display hangman
            self.hangman_display.config(text=self.display_hangman(6 - self.guesses_left))

        self.update_display()

        if self.check_win():
            messagebox.showinfo("Congratulations!", "You guessed the word! You win!")
            self.choose_word()
        elif self.check_loss():
            messagebox.showinfo("Game Over", f"Sorry, you ran out of guesses. The word was '{self.word_to_guess}'.")
            self.choose_word()

        # Update difficulty and guesses left info
        self.info_label.config(text=f"Difficulty: {self.difficulty.get().capitalize()} | Guesses Left: {self.guesses_left}")

    def check_win(self):
        return set(self.word_to_guess) <= self.guessed_letters

    def check_loss(self):
        return self.guesses_left <= 0

    def reset_game(self):
        self.choose_word()

    def display_hangman(self, incorrect_guesses):
        hangman_display = [
            "  +---+",
            "  |   |",
            "      |",
            "      |",
            "      |",
            "      |",
            "========="
        ]

        if incorrect_guesses >= 1:
            hangman_display[2] = "  O   |"

        if incorrect_guesses >= 2:
            hangman_display[3] = " /|\\  |"

        if incorrect_guesses >= 3:
            hangman_display[3] = " /|\\  |"
            hangman_display[4] = " /    |"

        if incorrect_guesses >= 4:
            hangman_display[3] = " /|\\  |"
            hangman_display[4] = " / \\  |"

        return "\n".join(hangman_display)

if __name__ == "__main__":
    root = tk.Tk()
    hangman_game = HangmanGame(root)
    root.mainloop()
