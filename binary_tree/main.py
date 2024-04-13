import tkinter as tk
from tkinter import messagebox
from lib import *


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.head = None
        self.current = None

    def create_widgets(self):
        self.entry = tk.Entry(self)
        self.entry.pack(side="top")

        self.add_button = tk.Button(self)
        self.add_button["text"] = "Add to List"
        self.add_button["command"] = self.add_to_list
        self.add_button.pack(side="top")

        self.bst_button = tk.Button(self)
        self.bst_button["text"] = "Create BST"
        self.bst_button["command"] = self.create_bst
        self.bst_button.pack(side="top")

        self.text = tk.Text(self)
        self.text.pack(side="bottom")

    def add_to_list(self):
        val = self.entry.get()
        if (val.isdigit() or (val.startswith("-") and val[1:].isdigit())) and (
            not self.current or self.current.val <= int(val)
        ):
            val = int(val)

            if not self.head:
                self.head = ListNode(val)
                self.current = self.head
            else:
                self.current.next = ListNode(val)
                self.current = self.current.next

            self.entry.delete(0, tk.END)
            self.text.insert(tk.END, f"Added {val} to list\n")
        else:
            messagebox.showerror(
                "Error", "Please enter a valid integer more than previous"
            )

    def create_bst(self):
        if not self.head:
            messagebox.showinfo("Info", "List is empty")
            return

        root = bst_from_list(self.head)
        self.display_tree(root)
        self.head = None  # Reset list after conversion
        self.current = None

    def display_tree(self, node, prefix="", pos="root"):
        if node:
            self.text.insert(
                tk.END, f"{prefix[:-4]}{'+---' if prefix else ''}{pos}: {node.val}\n"
            )
            self.display_tree(node.left, prefix + "|   ", "L")
            self.display_tree(node.right, prefix + "    ", "R")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
