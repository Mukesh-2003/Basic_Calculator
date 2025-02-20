import tkinter as tk
from tkinter import ttk
import ast
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2C3E50")

        self.expression = ""
        self.create_widgets()

    def create_widgets(self):
        self.display = ttk.Entry(self.root, font=("Arial", 20), justify='right')
        self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=10, ipady=10, sticky="nsew")

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('sqrt', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('^', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('sin', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('%', 4, 2), ('+', 4, 3), ('cos', 4, 4),
            ('C', 5, 0), ('del', 5, 1), ('=', 5, 2, 2), ('tan', 5, 4),
            ('bin', 6, 0), ('oct', 6, 1), ('hex', 6, 2), ('log', 6, 3), ('det', 6, 4)
        ]

        for button in buttons:
            text, row, col = button[:3]
            colspan = button[3] if len(button) > 3 else 1
            ttk.Button(self.root, text=text, command=lambda t=text: self.on_button_click(t), style='TButton')\
                .grid(row=row, column=col, columnspan=colspan, padx=5, pady=5, ipadx=10, ipady=10, sticky="nsew")

        for i in range(5):
            self.root.columnconfigure(i, weight=1)
        for i in range(7):
            self.root.rowconfigure(i, weight=1)

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 14), padding=5, background="#ECF0F1")

    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
        elif char == "del":
            self.expression = self.expression[:-1]
        elif char == "=":
            try:
                self.expression = self.safe_eval(self.expression)
            except Exception:
                self.expression = "Error"
        elif char in ["sqrt", "sin", "cos", "tan", "log"]:
            try:
                self.expression = str(self.calculate_function(char))
            except Exception:
                self.expression = "Error"
        elif char in ["bin", "oct", "hex"]:
            try:
                self.expression = self.convert_base(char)
            except Exception:
                self.expression = "Error"
        else:
            self.expression += str(char)
        self.update_display()

    def calculate_function(self, func):
        value = float(self.expression) if self.expression else 0
        if func == "sqrt":
            return math.sqrt(value)
        elif func == "sin":
            return math.sin(math.radians(value))
        elif func == "cos":
            return math.cos(math.radians(value))
        elif func == "tan":
            return math.tan(math.radians(value))
        elif func == "log":
            return math.log(value) if value > 0 else "Error"

    def convert_base(self, base):
        try:
            value = int(self.expression)
            if base == "bin":
                return bin(value)[2:]
            elif base == "oct":
                return oct(value)[2:]
            elif base == "hex":
                return hex(value)[2:].upper()
        except ValueError:
            return "Error"

    def safe_eval(self, expr):
        expr = expr.replace("^", "**")
        node = ast.parse(expr, mode='eval')
        return str(eval(compile(node, '<string>', 'eval')))

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    ScientificCalculator(root)
    root.mainloop()
