import tkinter as tk
from func.moduler import module_path
from func.rng import rng_range, rng_choice
import json

BG_COLORS = ["dark cyan", "cyan", "dark blue", "blue", "dark green", "green", "yellow", "dark orange", "orange", "dark red", "red", "dark magenta", "magenta", "dark violet", "violet", "dark gray", "gray", "black"]

NOTES_PATH = module_path("data/notes.json")

class StickyNotes(tk.Tk):
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

        titleBar = tk.Frame(note, bg=rng_choice(BG_COLORS), relief="raised", bd=2)
        titleBar.pack(side="top", fill="x")

        closeButton = tk.Button(titleBar, text="x", bg='dark gray', command=lambda: self.remove_note(note))
        closeButton.pack(side="right")

        def copy_text():
            if not text.tag_ranges("sel"):
                return
            selected_text = text.get("sel.first", "sel.last")
            self.clipboard_clear()
            self.clipboard_append(selected_text)

        def copy_all_text():
            if not text.tag_ranges("sel"):
                text.tag_add("sel", "1.0", "end")
            copy_text()
        
        def cut_text():
            copy_text()
            text.delete("sel.first", "sel.last")
        
        note.bind("<Control-c>", lambda _: copy_text())
        note.bind("<Control-a>", lambda _: text.tag_add("sel", "1.0", "end"))
        note.bind("<Control-x>", lambda _: cut_text())
        
        copyButton = tk.Button(titleBar, text="Copy", bg='dark gray', command=copy_all_text)
        copyButton.pack(side="right")

        text = tk.Text(note, height=10, width=40, font="Arial 12")
        text.pack()
        
        def on_drag_motion(event):
            x = note.winfo_x() + (event.x - note.getvar("x"))
            y = note.winfo_y() + (event.y - note.getvar("y"))
            note.geometry(f"+{x}+{y}")

        titleBar.bind("<ButtonPress-1>", lambda e: note.setvar("x", e.x) or note.setvar("y", e.y))
        titleBar.bind("<B1-Motion>", on_drag_motion)
        note.bind("<Destroy>", lambda _: self.remove_note(note))
        note.geometry(f"+{rng_range(0, self.winfo_screenwidth())}+{rng_range(0, self.winfo_screenheight())}")
        self.notes.append((note, text))
        return self.notes[-1]

    def remove_note(self, note):
        note.destroy()
        self.notes = [n for n in self.notes if n[0] != note]
    
    def get_text(self, text: tk.Text):
        return text.get("1.0", tk.END).rstrip()

    def save_notes(self):
        notes = []
        for note, text in self.notes:
            notes.append({"content": self.get_text(text), "size_and_pos": note.geometry()})
        json.dump(notes, open(NOTES_PATH, "w"), indent=4)

    def load_notes(self):
        self.notes = []
        try:
            for data in json.load(open(NOTES_PATH)):
                note, text = self.new_note()
                text.insert("1.0", data["content"])
                note.geometry(data["size_and_pos"])
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    app = StickyNotes()
    app.mainloop()
