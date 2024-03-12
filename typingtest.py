import tkinter as tk
import random
import time

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Test")
        self.root.geometry("700x300")  # Adjust the size for a better layout
        self.words_to_display = 5
        self.displayed_words = []
        self.test_active = False

        # Read words from file
        with open("wordlist.txt", "r") as file:
            self.words = file.read().splitlines()

        # UI setup
        self.setup_ui()

    def setup_ui(self):
        self.label_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.label_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.label = tk.Label(self.label_frame, text="Press Enter to start", font=("Helvetica", 16), anchor="w", justify=tk.LEFT, bg="#f0f0f0", fg="#333")
        self.label.pack(fill="both", expand=True)

        self.entry = tk.Entry(self.root, font=("Helvetica", 16), width=50, bd=3, relief="groove")
        self.entry.pack(pady=10)
        self.entry.bind("<space>", self.check_word)
        self.entry.bind("<Return>", self.start_test)
        self.entry.focus_set()

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#f0f0f0", fg="#333")
        self.result_label.pack(pady=10)

    def start_test(self, event=None):
        self.test_active = True
        self.start_time = time.time()
        self.total_words = 0
        self.correct_words = 0
        self.typed_words = 0
        self.entry.config(state="normal")
        self.result_label.config(text="")
        self.update_displayed_words()

    def update_displayed_words(self):
        self.displayed_words = random.choices(self.words, k=self.words_to_display)
        self.label.config(text=' '.join(self.displayed_words))
        self.entry.delete(0, tk.END)

    def check_word(self, event):
        if not self.test_active:
            return

        typed_word = self.entry.get().strip()
        if typed_word == self.displayed_words[0]:
            self.correct_words += 1
        self.typed_words += 1
        self.total_words += 1

        self.displayed_words.pop(0)
        self.displayed_words.extend(random.choices(self.words, k=1))
        self.label.config(text=' '.join(self.displayed_words))
        self.entry.delete(0, tk.END)

        if time.time() - self.start_time > 10:
            self.finish_test()

    def finish_test(self):
        self.test_active = False
        self.entry.config(state="disabled")
        accuracy = (self.correct_words / self.typed_words) * 100
        wpm = self.total_words / ((time.time() - self.start_time) / 60)
        result_text = f"Test Over. Accuracy: {accuracy:.2f}%, WPM: {wpm:.2f}\nPress Enter to restart."
        self.result_label.config(text=result_text)

# Create the main window
root = tk.Tk()
app = TypingTestApp(root)
root.mainloop()
