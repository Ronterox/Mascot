import tkinter as tk
from typing import List, Tuple

states_loop = [0, 0]
index = 0

def create_activities_loop(activities_loop: Tuple[List[str], List[str]]):
    root = tk.Tk()
    root.configure(bg="#000000", padx=10, pady=10)

    margin_right, margin_top = 60, 30
    x, y = root.winfo_screenwidth() - root.winfo_reqwidth() - margin_right, margin_top
    root.geometry(f"+{x}+{y}")

    def on_click(_):
        global index
        index = (index + 1) % 2

        # This is a HACK lol
        root.destroy()
        create_activities_loop(activities_loop)

    for i, activities in enumerate(activities_loop):
        bg, fg = ("green", "white") if i == index else ("#000000", "gray")

        fill = tk.Frame(root, bg=bg, height=20)
        fill.pack(fill=tk.X, pady=1)

        activity = activities[states_loop[i]]

        if activities == activities_loop[index]:
            states_loop[index] = (states_loop[index] + 1) % len(activities)

        label = tk.Label(fill, text=activity.upper(), bg=bg, fg=fg, font="Helvetica 20 bold")
        label.pack(fill=tk.X, padx=5, pady=5)

        label.bind("<Button-1>", on_click)

    print(states_loop)

    root.mainloop()

if __name__ == "__main__":
    activities_loop = (["watch video", "work project"], ["do task", "rest physical", "waifu chillax"])
    create_activities_loop(activities_loop)