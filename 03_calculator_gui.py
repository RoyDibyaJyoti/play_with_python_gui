import tkinter as tk
from tkinter import ttk
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("500x580")
        self.root.resizable(False, False)

        self.expression = ""
        self.just_evaluated = False

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')

        style.configure('Number.TButton', background='#add8e6', foreground='black', font=('Arial', 14, 'bold'))
        style.map('Number.TButton', background=[('active', '#87ceeb')])

        style.configure('Operator.TButton', background='#ffa500', foreground='white', font=('Arial', 14, 'bold'))
        style.map('Operator.TButton', background=[('active', '#ff8c00')])

        style.configure('Scientific.TButton', background='#32cd32', foreground='white', font=('Arial', 14, 'bold'))
        style.map('Scientific.TButton', background=[('active', '#228b22')])

        style.configure('Special.TButton', background='#ff4500', foreground='white', font=('Arial', 14, 'bold'))
        style.map('Special.TButton', background=[('active', '#e03e00')])

        style.configure('TEntry', font=('Arial', 20))

    def create_widgets(self):
        self.entry = ttk.Entry(self.root, justify="right", style='TEntry')
        self.entry.pack(fill=tk.X, ipadx=8, ipady=15, padx=10, pady=10)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        layout = [
            ['sqrt', 'log', 'sin', 'cos', 'tan'],
            ['rad', 'deg', 'pi', 'e', 'log10'],
            ['7', '8', '9', '(', ')'],
            ['4', '5', '6', '+', '-'],
            ['1', '2', '3', '*', '/'],
            ['clr', '0', '←', '^', '%'],
            ['deg(x)', 'rad(x)', 'tau', '=', '']
        ]

        for r, row in enumerate(layout):
            for c, label in enumerate(row):
                if label == '':
                    continue
                colspan = 2 if label == '=' else 1

                style = 'Number.TButton'
                if label in ['+', '-', '*', '/', '^', '%']:
                    style = 'Operator.TButton'
                elif label in ['clr', '←', '=']:
                    style = 'Special.TButton'
                elif label.replace('(', '').replace(')', '') in dir(math) or label in ['pi', 'e', 'tau', 'rad', 'deg', 'deg(x)', 'rad(x)', 'log10']:
                    style = 'Scientific.TButton'

                btn = ttk.Button(btn_frame, text=label, style=style, command=lambda ch=label: self.on_click(ch))
                btn.grid(row=r, column=c, columnspan=colspan, sticky='nsew', padx=3, pady=3)
                if colspan == 2:
                    break

        for r in range(len(layout)):
            btn_frame.rowconfigure(r, weight=1)
        for c in range(5):
            btn_frame.columnconfigure(c, weight=1)

    def on_click(self, char):
        operators = ['/', '*', '-', '+', '**', '^', '%']
        functions = ['sqrt', 'log', 'log10', 'sin', 'cos', 'tan', 'rad', 'deg', 'deg(x)', 'rad(x)']

        if char == 'clr':
            self.expression = ""
            self.just_evaluated = False
        elif char == '←':
            if self.just_evaluated:
                self.expression = ""
                self.just_evaluated = False
            else:
                self.expression = self.expression[:-1]
        elif char == '=':
            self.evaluate_expression()
            return
        elif char == 'pi':
            self.expression = str(math.pi) if self.just_evaluated else self.expression + str(math.pi)
            self.just_evaluated = False
        elif char == 'e':
            self.expression = str(math.e) if self.just_evaluated else self.expression + str(math.e)
            self.just_evaluated = False
        elif char == 'tau':
            self.expression = str(math.tau) if self.just_evaluated else self.expression + str(math.tau)
            self.just_evaluated = False
        elif char == '^':
            self.expression += '**'
            self.just_evaluated = False
        elif char in functions:
            if char == 'deg(x)':
                self.expression += "math.degrees("
            elif char == 'rad(x)':
                self.expression += "math.radians("
            else:
                self.expression += f"{char}("
            self.just_evaluated = False
        else:
            if self.just_evaluated and (char.isdigit() or char == '.'):
                self.expression = char
            else:
                self.expression += char
            self.just_evaluated = False

        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.expression)

    def evaluate_expression(self):
        try:
            allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
            allowed_names.update({"abs": abs, "round": round})
            result = eval(self.expression, {"__builtins__": None}, allowed_names)
            self.expression = str(result)
        except Exception:
            self.expression = "Error"
        self.just_evaluated = True
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.expression)


if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()
