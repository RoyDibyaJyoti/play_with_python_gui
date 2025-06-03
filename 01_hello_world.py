import tkinter as tk

class HelloWorldApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hello World GUI")
        self.root.geometry("400x150+200+100")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # Label to instruct user
        self.instruction_label = tk.Label(self.root, text="Click the Button")
        self.instruction_label.pack(pady=(20, 5))

        # Label to display message
        self.label = tk.Label(self.root, text="", font=("Times", 20))
        self.label.pack(pady=5)

        # Button to trigger message display
        self.button = tk.Button(self.root, text="Click Me!", command=self.show_hello)
        self.button.pack(pady=5)

    def show_hello(self):
        self.label.config(text="Hello, World!")

if __name__ == "__main__":
    root = tk.Tk()
    app = HelloWorldApp(root)
    root.mainloop()
