import tkinter as tk
from math import sin, cos, tan, log, log10, sqrt, degrees, radians, pi, e, tau
import re

class NeumorphicButton(tk.Canvas):
    def __init__(self, master, text, diameter=70, fill_color="#e0e0e0", text_color="#333333",
                 shadow_light="#ffffff", shadow_dark="#a3b1c6", command=None, shape="circle"):
        width = diameter * 2 if shape == "rounded_rect" else diameter
        height = diameter
        super().__init__(master, width=width, height=height, highlightthickness=0, bg=master['bg'])

        self.text = text
        self.diameter = diameter
        self.fill_color = fill_color
        self.text_color = text_color
        self.shadow_light = shadow_light
        self.shadow_dark = shadow_dark
        self.command = command
        self.shape = shape
        self.pressed = False

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

        self._draw_button()

    def _draw_button(self):
        self.delete("all")
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        if self.shape == "circle":
            # Outer shadows
            if not self.pressed:
                self.create_oval(8, 8, w, h, fill=self.shadow_dark, outline='')
                self.create_oval(0, 0, w-8, h-8, fill=self.shadow_light, outline='')
            else:
                self.create_oval(8, 8, w, h, fill=self.shadow_light, outline='')
                self.create_oval(0, 0, w-8, h-8, fill=self.shadow_dark, outline='')

            # Main circle colored button
            self.create_oval(4, 4, w-4, h-4, fill=self.fill_color, outline='')
        else:
            # Rounded rectangle for '=' button
            r = 20
            def rounded_rect(x1, y1, x2, y2, r, **kwargs):
                self.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, style=tk.PIESLICE, **kwargs)
                self.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, style=tk.PIESLICE, **kwargs)
                self.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, style=tk.PIESLICE, **kwargs)
                self.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, style=tk.PIESLICE, **kwargs)
                self.create_rectangle(x1+r, y1, x2-r, y2, **kwargs)
                self.create_rectangle(x1, y1+r, x2, y2-r, **kwargs)

            if not self.pressed:
                rounded_rect(8, 8, w, h, r, fill=self.shadow_dark, outline='')
                rounded_rect(0, 0, w-8, h-8, r, fill=self.shadow_light, outline='')
            else:
                rounded_rect(8, 8, w, h, r, fill=self.shadow_light, outline='')
                rounded_rect(0, 0, w-8, h-8, r, fill=self.shadow_dark, outline='')

            rounded_rect(4, 4, w-4, h-4, r, fill=self.fill_color, outline='')

        # Text
        self.create_text(w // 2, h // 2, text=self.text, fill=self.text_color, font=('Segoe UI', 16, 'bold'))

    def _on_press(self, event):
        self.pressed = True
        self._draw_button()

    def _on_release(self, event):
        self.pressed = False
        self._draw_button()
        if self.command:
            self.command(self.text)


def insert_implicit_multiplication(expr):
    # Insert * between number and '('
    expr = re.sub(r'(\d)(\()', r'\1*\2', expr)
    # Insert * between ')' and number
    expr = re.sub(r'(\))(\d)', r'\1*\2', expr)
    # Insert * between ')' and '('
    expr = re.sub(r'(\))(\()', r'\1*\2', expr)
    return expr


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Neumorphic Calculator")
        self.geometry("420x700")
        self.resizable(False, False)

        self.expression = ""
        self.just_evaluated = False

        self.themes = {
            "light": {
                "bg": "#e0e0e0", "fg": "#333333",
                "shadow_light": "#ffffff", "shadow_dark": "#a3b1c6",
            },
            "dark": {
                "bg": "#2e2e2e", "fg": "#e0e0e0",
                "shadow_light": "#3a3a3a", "shadow_dark": "#1e1e1e",
            }
        }
        self.current_theme = "light"
        self.configure(bg=self.themes[self.current_theme]["bg"])

        self._create_menu()
        self._create_widgets()
        self._create_theme_toggle()
        self._bind_keys()

    def _create_menu(self):
        menubar = tk.Menu(self)
        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Light", command=lambda: self._change_theme("light"))
        theme_menu.add_command(label="Dark", command=lambda: self._change_theme("dark"))
        menubar.add_cascade(label="Theme", menu=theme_menu)
        self.config(menu=menubar)

    def _change_theme(self, theme_name):
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        self.configure(bg=theme["bg"])
        self.entry.config(bg=theme["bg"], fg=theme["fg"], insertbackground=theme["fg"])
        self.btn_frame.config(bg=theme["bg"])
        self.theme_btn.config(bg=theme["bg"], fg=theme["fg"])
        for label, btn in self.buttons.items():
            fill, fg = self._get_button_colors(label, theme_name)
            btn.fill_color = fill
            btn.text_color = fg
            btn.shadow_light = theme["shadow_light"]
            btn.shadow_dark = theme["shadow_dark"]
            btn.config(bg=theme["bg"])
            btn._draw_button()

    def _get_button_colors(self, label, theme_name):
        if theme_name == "light":
            colors = {
                "scientific": ("#f4a261", "#ffffff"),
                "numbers": ("#2a9d8f", "#ffffff"),
                "operators": ("#e76f51", "#ffffff"),
                "special": ("#264653", "#ffffff"),
                "equal": ("#1b4332", "#ffffff"),
            }
        else:
            colors = {
                "scientific": ("#e76f51", "#000000"),
                "numbers": ("#2a9d8f", "#000000"),
                "operators": ("#f4a261", "#000000"),
                "special": ("#a8dadc", "#000000"),
                "equal": ("#52b788", "#000000"),
            }

        scientific = {"sqrt", "log", "sin", "cos", "tan", "rad", "deg", "pi", "e", "log10", "deg(x)", "rad(x)", "tau"}
        numbers = {"0","1","2","3","4","5","6","7","8","9"}
        operators = {"+", "-", "*", "/", "^", "%", "(", ")"}
        special = {"clr", "←"}
        equal = {"="}

        if label in scientific:
            return colors["scientific"]
        elif label in numbers:
            return colors["numbers"]
        elif label in operators:
            return colors["operators"]
        elif label in special:
            return colors["special"]
        elif label in equal:
            return colors["equal"]
        else:
            return (self.themes[self.current_theme]["bg"], self.themes[self.current_theme]["fg"])

    def _create_widgets(self):
        theme = self.themes[self.current_theme]
        self.entry = tk.Entry(self, font=('Segoe UI', 24), bd=0, justify='right',
                              bg=theme["bg"], fg=theme["fg"], insertbackground=theme["fg"])
        self.entry.place(x=10, y=20, width=400, height=50)

        layout = [
            ["sqrt", "log", "sin", "cos", "tan"],
            ["rad", "deg", "pi", "e", "log10"],
            ["7", "8", "9", "(", ")"],
            ["4", "5", "6", "+", "-"],
            ["1", "2", "3", "*", "/"],
            ["clr", "0", "←", "^", "%"],
            ["deg(x)", "rad(x)", "tau", "=", "="]
        ]

        btn_w = 70
        btn_h = 70
        padding = 10

        self.btn_frame = tk.Frame(self, bg=theme["bg"])
        self.btn_frame.place(x=10, y=110, width=400, height=570)

        self.buttons = {}

        for r, row in enumerate(layout):
            for c, label in enumerate(row):
                shape = 'circle'
                colspan = 1
                if label == "=" and c == 3:
                    shape = "rounded_rect"
                    colspan = 2
                if label == "=" and c == 4:
                    continue

                x = c * (btn_w + padding)
                y = r * (btn_h + padding)

                width = btn_w * colspan + padding * (colspan - 1)
                height = btn_h

                fill_color, text_color = self._get_button_colors(label, self.current_theme)

                btn = NeumorphicButton(
                    self.btn_frame, label, diameter=btn_h,
                    fill_color=fill_color, text_color=text_color,
                    shadow_light=theme["shadow_light"], shadow_dark=theme["shadow_dark"],
                    command=self._on_button_click, shape=shape
                )
                btn.place(x=x, y=y, width=width, height=height)
                self.buttons[label] = btn

    def _create_theme_toggle(self):
        theme = self.themes[self.current_theme]
        self.theme_btn = tk.Button(self, text=f"Theme: {self.current_theme.title()}",
                                   command=self._toggle_theme,
                                   bg=theme["bg"], fg=theme["fg"],
                                   relief=tk.FLAT, font=('Segoe UI', 12))
        self.theme_btn.place(x=150, y=680, width=120, height=25)

    def _toggle_theme(self):
        new_theme = "dark" if self.current_theme == "light" else "light"
        self._change_theme(new_theme)
        self.theme_btn.config(text=f"Theme: {new_theme.title()}")

    def _on_button_click(self, char):
        funcs = {'sin', 'cos', 'tan', 'log', 'log10', 'sqrt', 'deg(x)', 'rad(x)'}
        specials = {'clr', '←', '='}
        constants = {'pi': str(pi), 'e': str(e), 'tau': str(tau)}

        if char == 'clr':
            self.expression = ''
            self.just_evaluated = False
        elif char == '←':
            if self.just_evaluated:
                self.expression = ''
                self.just_evaluated = False
            else:
                self.expression = self.expression[:-1]
        elif char == '=':
            self._evaluate()
            return
        elif char in constants:
            if self.just_evaluated:
                self.expression = constants[char]
            else:
                self.expression += constants[char]
            self.just_evaluated = False
        elif char == '^':
            self.expression += '**'
            self.just_evaluated = False
        elif char in funcs:
            if char == 'deg(x)':
                self.expression += 'degrees('
            elif char == 'rad(x)':
                self.expression += 'radians('
            else:
                self.expression += f"{char}("
            self.just_evaluated = False
        else:
            if self.just_evaluated and (char.isdigit() or char == '.'):
                self.expression = char
            else:
                self.expression += char
            self.just_evaluated = False

        self._update_entry()

    def _update_entry(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.expression)

    def _evaluate(self):
        try:
            allowed_names = {k: v for k, v in globals().items() if k in
                             ['sin', 'cos', 'tan', 'sqrt', 'log', 'log10', 'radians', 'degrees', 'pi', 'e', 'tau']}
            expr = insert_implicit_multiplication(self.expression)
            self.expression = str(eval(expr, {"__builtins__": {}}, allowed_names))
        except Exception:
            self.expression = "Error"
        self.just_evaluated = True
        self._update_entry()

    def _bind_keys(self):
        self.bind("<Key>", self._handle_key)

    def _handle_key(self, event):
        if event.keysym == "Return":
            self._evaluate()
        elif event.keysym == "BackSpace":
            self._on_button_click("←")
        elif event.char in "0123456789.+-*/()%^":
            self._on_button_click(event.char)


if __name__ == "__main__":
    Calculator().mainloop()