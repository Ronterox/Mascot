import random
import tkinter as tk

class StickyNote(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sticky Note")

        self.notes = []

        try:
            with open("note.txt", "r") as f:
                for note_content, x, y in map(lambda l: l.strip().split("|"), f.readlines()):
                    self.new_note()
                    self.notes[-1][1].insert(tk.END, note_content)
                    self.notes[-1][0].geometry(f"+{x}+{y}")
        except:
            pass

        new_button = tk.Button(self, text="New", command=self.new_note)
        new_button.pack()

        save_button = tk.Button(self, text="Save", command=self.save_note)
        save_button.pack()

    def new_note(self):
        note = tk.Toplevel(self)
        note.geometry(f"+{random.randint(0, self.winfo_screenwidth())}+{random.randint(0, self.winfo_screenheight())}")
        text = tk.Text(note, height=10, width=40)
        note.attributes('-topmost', True)
        note.bind("<Destroy>", lambda event: self.remove_note(event, note))
        text.pack()
        self.notes.append((note, text))


    def remove_note(self, event, note):
        note.destroy()
        notes = [n for n in self.notes if n[0] != note]


    def save_note(self):
        with open("note.txt", "w") as f:
            for note, text in self.notes:
                note_content = text.get("1.0", tk.END).rstrip()
                x, y = map(int, note.geometry().split("+")[1:])
                f.write(f"{note_content}|{x}|{y}\n")

if __name__ == '__main__':
    app = StickyNote()
    app.mainloop()
