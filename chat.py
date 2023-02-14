import tkinter as tk

class ChatWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Set the title and dimensions of the window
        self.master.title("Chat Window")
        self.master.geometry("400x600")

        # Create the widgets for the chat window
        self.message_frame = tk.Frame(self)
        self.message_box = tk.Text(self.message_frame, height=15, width=50)
        self.message_scroll = tk.Scrollbar(self.message_frame, orient=tk.VERTICAL, command=self.message_box.yview)
        self.message_box['yscrollcommand'] = self.message_scroll.set
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.message_input = tk.Entry(self, width=50)

        # Lay out the widgets in the window
        self.message_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.message_box.pack(side=tk.LEFT, fill=tk.BOTH)
        self.message_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_input.pack(side=tk.BOTTOM, fill=tk.X)
        self.send_button.pack(side=tk.BOTTOM)

    def send_message(self):
        # Get the message from the input field and add it to the chat box
        message = self.message_input.get()
        self.message_box.insert(tk.END, message + "\n")

        # Clear the input field
        self.message_input.delete(0, tk.END)

# Create the main window and the floating chat window
root = tk.Tk()
chat_window = ChatWindow(root)
chat_window.pack()

# Run the Tkinter event loop
root.mainloop()
