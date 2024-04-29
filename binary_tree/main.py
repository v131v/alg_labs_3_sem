import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from lib import *
import math


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.head = None
        self.current = None
        self._vertex = list()
        self._edge = list()
        self.r = 15

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

        self.res_label = ttk.Label(
            self, text="There will be list...", foreground=light, background=dark
        )
        self.res_label.pack(fill="x", expand=True)

        self.canvas = tk.Canvas(
            self, width=600, height=400, bg="#853c85", highlightbackground=dark
        )
        self.canvas.pack(side=tk.TOP)

        self.entry = ttk.Entry(self)
        self.entry.pack(side="top")

        self.add_button = ttk.Button(self, text="Add to List", command=self.add_to_list)
        self.add_button.pack(side="top")

        self.bst_button = ttk.Button(self, text="Create BST", command=self.create_bst)
        self.bst_button.pack(side="top")

        self.text = ttk.Label(self)
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

                self.res_label.configure(text=f"({val})")
            else:
                self.current.next = ListNode(val)
                self.current = self.current.next

                self.res_label.configure(text=self.res_label["text"] + f" -> ({val})")
        else:
            messagebox.showerror(
                "Error", "Please enter a valid integer more than previous"
            )

    def create_bst(self):
        if not self.head:
            messagebox.showinfo("Info", "List is empty")
            return

        root = bst_from_list(self.head)
        print(int(self.canvas["width"]))
        self._edge = list()
        self._vertex = list()
        self.dfs(root, 0, int(self.canvas["width"]), 1)

        self.draw()
        self.head = None  # Reset list after conversion
        self.current = None

    def dfs(self, cur: TreeNode | None, l: int, r: int, h: int) -> int:
        if cur is None:
            return None

        m = (r - l) // 2 + l
        cur_id = len(self._vertex)
        self._vertex.append({"x": m, "y": h * 40, "id": cur_id, "val": cur.val})

        if cur.left is not None:
            l_id = self.dfs(cur.left, l, m, h + 1)
            self._edge.append({"from": cur_id, "to": l_id})

        if cur.right is not None:
            r_id = self.dfs(cur.right, m, r, h + 1)
            self._edge.append({"from": cur_id, "to": r_id})

        print(self._edge)

        return cur_id

    def display_tree(self, node, prefix="", pos="root"):
        if node:
            self.text.insert(
                tk.END, f"{prefix[:-4]}{'+---' if prefix else ''}{pos}: {node.val}\n"
            )
            self.display_tree(node.left, prefix + "|   ", "L")
            self.display_tree(node.right, prefix + "    ", "R")

    def draw(self):
        self.canvas.delete("all")

        for v in self._vertex:
            self.draw_vertex(v)

        for e in self._edge:
            self.draw_edge(e)

    def draw_vertex(self, vertex: dict) -> None:  # рисование вершины в canvas
        x, y = vertex["x"], vertex["y"]
        self.canvas.create_oval(
            x - self.r, y - self.r, x + self.r, y + self.r, outline=self.light
        )
        self.canvas.create_text(x, y, text=str(vertex["val"]), fill=self.light)

    def draw_edge(self, edge: dict, dark: bool = False) -> None:  # отображение ребра
        color = self.dark if dark else self.light

        from_vertex, to_vertex = edge["from"], edge["to"]

        from_x, from_y = self.get_vertex_coordinates(
            from_vertex
        )  # получение координат исходящей вершины
        to_x, to_y = self.get_vertex_coordinates(
            to_vertex
        )  # получение координат входящей вершины

        # отображение ребраweight
        dx = to_x - from_x
        dy = to_y - from_y
        l = (dx**2 + dy**2) ** 0.5

        ang = math.atan2(dy, dx)

        from_x += math.cos(ang) * self.r
        from_y += math.sin(ang) * self.r

        to_x -= math.cos(ang) * self.r
        to_y -= math.sin(ang) * self.r

        l2 = l / 20

        x1 = l2 * math.cos(ang + math.pi + math.pi / 4)
        y1 = l2 * math.sin(ang + math.pi + math.pi / 4)
        self.canvas.create_line(
            to_x, to_y, to_x + x1, to_y + y1, width=3, fill=color, tag="line"
        )

        x1 = l2 * math.cos(ang + math.pi - math.pi / 4)
        y1 = l2 * math.sin(ang + math.pi - math.pi / 4)
        self.canvas.create_line(
            to_x, to_y, to_x + x1, to_y + y1, width=3, fill=color, tag="line"
        )

        self.canvas.create_line(
            from_x, from_y, to_x, to_y, width=3, fill=color, tag="line"
        )

        line = self.canvas.create_line(
            from_x, from_y, to_x, to_y, width=3, fill=color, tag="line"
        )

        self.canvas.tag_lower(line)

    def get_vertex_coordinates(self, vertex: int) -> tuple:  # получение координат точки
        return (self._vertex[vertex]["x"], self._vertex[vertex]["y"])


if __name__ == "__main__":
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()
