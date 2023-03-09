import tkinter as tk
from rng import rng_range
import json


class StickyNote(tk.Tk):
    notes = []

    def __init__(self):
        super().__init__()
        self.title("Sticky Note")
        self.wm_maxsize(100, 50)
        self.load_notes()
        self.create_button("New", self.new_note)
        self.create_button("Save", self.save_notes)

    def create_button(self, text, command):
        button = tk.Button(self, text=text, command=command)
        button.pack()

    def new_note(self):
        note = tk.Toplevel(self)
        note.overrideredirect(True)
        note.geometry(f"+{rng_range(0, self.winfo_screenwidth())}+{rng_range(0, self.winfo_screenheight())}")
        closeButton = tk.Button(note, text="Close", command=lambda: self.remove_note(note))
        closeButton.pack()
        text = tk.Text(note, height=10, width=40, font="Arial 12")
        text.pack()
        note.bind("<Destroy>", lambda _: self.remove_note(note))
        self.notes.append((note, text))
        return self.notes[-1]

    def remove_note(self, note):
        note.destroy()
        self.notes = [n for n in self.notes if n[0] != note]

    def save_notes(self):
        notes = []
        for note, text in self.notes:
            notes.append({"content": text.get("1.0", tk.END).rstrip(), "size_and_pos": note.geometry()})
        json.dump(notes, open("notes.json", "w"), indent=4)


    def load_notes(self):
        try:
            for data in json.load(open("notes.json")):
                note, text = self.new_note()
                text.insert("1.0", data["content"])
                note.geometry(data["size_and_pos"])
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    app = StickyNote()
    app.mainloop()
