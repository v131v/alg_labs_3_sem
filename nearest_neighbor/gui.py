import tkinter as tk
from tkinter import ttk
import math
from typing import Callable, Tuple


class App:
    def __init__(
        self,
        title: str,
        handler: Callable[
            [int, list[Tuple[int, int, float]]],
            Tuple[list[Tuple[int, int, float], float]],
        ],
    ) -> None:

        self._edge = list(
            [
                {"from": 1, "to": 2, "weight": 1},
                {"from": 2, "to": 3, "weight": 2},
                {"from": 3, "to": 1, "weight": 3},
            ]
        )  # список ребер
        self._vertex = list(
            [
                {"x": 50, "y": 50, "id": 1},
                {"x": 300, "y": 50, "id": 2},
                {"x": 300, "y": 300, "id": 3},
            ]
        )  # список вершин
        self._selected_edge = list()

        self._handler = handler

        # интерфейс
        light = "#f33ff3"
        dark = "#562c56"

        self.light = light
        self.dark = dark

        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.configure(bg=dark)

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

        self.canvas = tk.Canvas(
            self.root, width=600, height=400, bg="#853c85", highlightbackground=dark
        )
        self.canvas.pack(side=tk.TOP)

        self.from_label = ttk.Label(
            self.root, text="From:", foreground=light, background=dark
        )
        self.from_label.pack()
        self.from_entry = ttk.Entry(self.root)
        self.from_entry.pack()

        self.to_label = ttk.Label(
            self.root, text="To:", foreground=light, background=dark
        )
        self.to_label.pack()
        self.to_entry = ttk.Entry(self.root)
        self.to_entry.pack()

        self.weight_label = ttk.Label(
            self.root, text="Weight:", foreground=light, background=dark
        )
        self.weight_label.pack()
        self.weight_entry = ttk.Entry(self.root)
        self.weight_entry.pack()

        self.add_button = ttk.Button(self.root, text="Set edge", command=self.add_edge)
        self.add_button.pack()

        self.add_button = ttk.Button(
            self.root,
            text="Find path",
            command=self.run,
        )
        self.add_button.pack()

        self.canvas.bind("<Button-1>", self.add_vertex)

        self.root.mainloop()

    def add_vertex(
        self, event
    ) -> None:  # считывание нажатия и добавления в точку новой вершины
        x, y = event.x, event.y  # получение координат
        self._vertex.append({"x": x, "y": y, "id": len(self._vertex) + 1})
        self.draw()

    def add_edge(self) -> None:  # добавление ребра
        from_vertex = int(self.from_entry.get())  # считывание данных
        to_vertex = int(self.to_entry.get())
        weight = int(self.weight_entry.get())

        if not (
            from_vertex > 0
            and from_vertex <= len(self._vertex)
            and to_vertex > 0
            and to_vertex <= len(self._vertex)
        ):
            return

        for i in range(len(self._edge)):
            if (
                self._edge[i]["from"] == from_vertex
                and self._edge[i]["to"] == to_vertex
            ):
                self._edge[i], self._edge[-1] = self._edge[-1], self._edge[i]
                self._edge = self._edge[:-1]
                break

        self._edge.append(
            {"from": from_vertex, "to": to_vertex, "weight": weight}
        )  # добавление ребра в список

        self.draw()

    def draw(self):
        self.canvas.delete("all")

        for v in self._vertex:
            self.draw_vertex(v)

        for e in self._edge:
            self.draw_edge(e)

        for e in self._selected_edge:
            self.draw_edge(e, True)

    def draw_vertex(self, vertex: dict) -> None:  # рисование вершины в canvas
        x, y = vertex["x"], vertex["y"]
        self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, outline=self.light)
        self.canvas.create_text(x, y, text=str(vertex["id"]), fill=self.light)

    def draw_edge(self, edge: dict, dark: bool = False) -> None:  # отображение ребра
        color = self.dark if dark else self.light

        from_vertex, to_vertex, weight = edge["from"], edge["to"], edge["weight"]

        from_x, from_y = self.get_vertex_coordinates(
            from_vertex
        )  # получение координат исходящей вершины
        to_x, to_y = self.get_vertex_coordinates(
            to_vertex
        )  # получение координат входящей вершины

        # отображение ребра
        dx = to_x - from_x
        dy = to_y - from_y
        l = (dx**2 + dy**2) ** 0.5

        ang = math.atan2(dy, dx)

        from_x += math.cos(ang) * 30
        from_y += math.sin(ang) * 30

        to_x -= math.cos(ang) * 30
        to_y -= math.sin(ang) * 30

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

        self.canvas.create_text(
            (to_x + from_x) / 2 + math.cos(ang + math.pi / 2) * l2,
            (to_y + from_y) / 2 + math.sin(ang + math.pi / 2) * l2,
            text=str(weight),
            fill=color,
        )
        self.canvas.tag_lower(line)

    def get_vertex_coordinates(self, vertex: int) -> tuple:  # получение координат точки
        return (self._vertex[vertex - 1]["x"], self._vertex[vertex - 1]["y"])

    def run(self):  # запуск алгоритма
        selected_edge, dist = self._handler(
            len(self._vertex),
            [(e["from"] - 1, e["to"] - 1, float(e["weight"])) for e in self._edge],
        )

        if dist == float("inf"):
            self.canvas.create_text(300, 10, text=f"Distance: {dist}", fill=self.light)
            return

        self._selected_edge = [
            {
                "from": f + 1,
                "to": t + 1,
                "weight": int(w),
            }
            for f, t, w in selected_edge
        ]

        # self.canvas.delete("all")

        self.draw()

        tour = "-".join([str(x["from"]) for x in self._selected_edge])

        self.canvas.create_text(300, 10, text=f"Distance: {dist}", fill=self.light)
        self.canvas.create_text(300, 25, text=f"Path: {tour}", fill=self.light)
