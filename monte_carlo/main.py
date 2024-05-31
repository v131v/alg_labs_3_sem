import tkinter as tk
from tkinter import ttk
from lib import *


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):

        light = "#f33ff3"
        dark = "#562c56"

        self.light = light
        self.dark = dark

        styleBtn = ttk.Style()
        styleBtn.theme_use("clam")
        styleBtn = styleBtn.configure(
            "TButton", foreground=light, background=dark, bordercolor=light
        )

        styleEntry = ttk.Style()
        styleEntry.theme_use("clam")
        styleEntry = styleEntry.configure(
            "TEntry", foreground=light, background=dark, bordercolor=light
        )

        styleLabel = ttk.Style()
        styleLabel.theme_use("clam")
        styleLabel = styleLabel.configure("TLabel", foreground=light, background=dark)

        self.configure(bg=dark)

        ttk.Label(self, text="Iterations count (N):").pack(expand=True)
        self.entry_n = ttk.Entry(self)
        self.entry_n.pack(expand=True)

        self.calculate_button = ttk.Button(
            self,
            text="Calc area of { -x**3 + y**5 < 2, x-y < 1 }",
            command=self.calculate_area,
        )
        self.calculate_button.pack(expand=True)

        self.calculate_button = ttk.Button(
            self, text="Calc integral of f = x**3", command=self.calculate_integral
        )
        self.calculate_button.pack(expand=True)

        self.result_label = ttk.Label(self, text="")
        self.result_label.pack(expand=True)

        self.error_label = ttk.Label(self, text="")
        self.error_label.pack(expand=True)

    def calculate_area(self):
        n = self.get_count()
        result, relative_error = monte_carlo_area(n)
        self.result_label.config(text=f"Area: {result:.5f}")
        self.error_label.config(text=f"Relative error: {relative_error:.5f}")

    def calculate_integral(self):
        n = self.get_count()
        result, relative_error = monte_carlo_integral(n)
        self.result_label.config(text=f"Integral: {result:.5f}")
        self.error_label.config(text=f"Relative error: {relative_error:.5f}")

    def get_count(self):
        try:
            n = int(self.entry_n.get())
            if n < 0:
                raise ValueError()
            return n
        except ValueError:
            self.result_label.config(text="Error: enter integer count > 0")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
