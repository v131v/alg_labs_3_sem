import tkinter as tk
from tkinter import ttk
import math
from typing import Callable, Tuple


class App:
    def __init__(
        self,
        title: str,
        handler: Callable[
            [int, list[Tuple[int, int, float]], float, float],
            Tuple[list[Tuple[int, int, float], float]],
        ],
    ) -> None:

        self._edge = list(
            [
                {"from": 1, "to": 2, "weight": 1},
                {"from": 2, "to": 3, "weight": 2},
                {"from": 3, "to": 1, "weight": 3},
                {"from": 2, "to": 4, "weight": 1},
                {"from": 4, "to": 3, "weight": 1},
            ]
        )  # список ребер
        self._vertex = list(
            [
                {"x": 50, "y": 50, "id": 1},
                {"x": 300, "y": 50, "id": 2},
                {"x": 300, "y": 300, "id": 3},
                {"x": 400, "y": 200, "id": 4},
            ]
        )  # список вершин
        self._selected_edge = list()

        self._edge = list(
            [
                {"from": 1, "to": 2, "weight": 3},
                {"from": 1, "to": 5, "weight": 1},
                {"from": 1, "to": 6, "weight": 2},
                {"from": 2, "to": 1, "weight": 3},
                {"from": 2, "to": 6, "weight": 3},
                {"from": 2, "to": 3, "weight": 8},
                {"from": 3, "to": 2, "weight": 3},
                {"from": 3, "to": 6, "weight": 3},
                {"from": 3, "to": 4, "weight": 1},
                {"from": 4, "to": 3, "weight": 8},
                {"from": 4, "to": 5, "weight": 1},
                {"from": 5, "to": 1, "weight": 3},
                {"from": 5, "to": 4, "weight": 3},
                {"from": 5, "to": 6, "weight": 4},
                {"from": 6, "to": 1, "weight": 3},
                {"from": 6, "to": 2, "weight": 3},
                {"from": 6, "to": 3, "weight": 3},
                {"from": 6, "to": 4, "weight": 5},
            ]
        )
        self._vertex = list(
            [
                {"x": 101, "y": 50, "id": 1},
                {"x": 200, "y": 51, "id": 2},
                {"x": 302, "y": 200, "id": 3},
                {"x": 200, "y": 302, "id": 4},
                {"x": 103, "y": 300, "id": 5},
                {"x": 50, "y": 203, "id": 6},
            ]
        )

        self._handler = handler

        # интерфейс
        light = "#f33ff3"
        dark = "#562c56"

        self.light = light
        self.dark = dark

        self.root = tk.Tk()
        self.root.title(title)
        # self.root.geometry("600x600")
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

        styleScale = ttk.Style()
        styleScale.theme_use("clam")
        styleScale = styleScale.configure(
            "Vertical.TScale",
            foreground=light,
            background=dark,
            bordercolor=light,
            troughcolor=dark,
            darkcolor=dark,
            lightcolor=light,
            highlightbackground=light,
        )

        self.res_label = ttk.Label(
            self.root, text="There will be result...", foreground=light, background=dark
        )
        self.res_label.pack(fill="x", expand=True)

        self.canvas = tk.Canvas(
            self.root, width=600, height=400, bg="#853c85", highlightbackground=dark
        )
        self.canvas.pack(side=tk.TOP)

        self.frame = tk.Frame(self.root, bg=dark)
        self.frame.pack(side="left", fill="both", expand=True)

        self.from_label = ttk.Label(self.frame, text="From:")
        self.from_label.pack()
        self.from_entry = ttk.Entry(self.frame)
        self.from_entry.pack()

        self.to_label = ttk.Label(self.frame, text="To:")
        self.to_label.pack()
        self.to_entry = ttk.Entry(self.frame)
        self.to_entry.pack()

        self.weight_label = ttk.Label(self.frame, text="Weight:")
        self.weight_label.pack()
        self.weight_entry = ttk.Entry(self.frame)
        self.weight_entry.pack()

        self.add_button = ttk.Button(self.frame, text="Set edge", command=self.add_edge)
        self.add_button.pack()

        self.add_button = ttk.Button(
            self.frame,
            text="Find path",
            command=self.start_algoritm,
        )
        self.add_button.pack()

        self.frame2 = tk.Frame(self.root, bg=dark)
        self.frame2.pack(side="left", fill="both", expand=True)

        self.alpha_label = ttk.Label(self.frame2, text="Alpha:")
        self.alpha_label.pack()
        self.alpha_entry = ttk.Entry(self.frame2)
        self.alpha_entry.pack()

        self.beta_label = ttk.Label(self.frame2, text="Beta:")
        self.beta_label.pack()
        self.beta_entry = ttk.Entry(self.frame2)
        self.beta_entry.pack()

        self.canvas.bind("<Button-1>", self.add_vertex)

        self.root.mainloop()

    def upd_tempreture(self, val):
        self.tempr_label.configure(text=f"Tempreture: {int(float(val))}")
        self.draw()

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

    def start_algoritm(self):  # запуск алгоритма
        selected_edge, dist = self._handler(
            len(self._vertex),
            [(e["from"] - 1, e["to"] - 1, float(e["weight"])) for e in self._edge],
            float(self.alpha_entry.get()),
            float(self.beta_entry.get()),
        )

        if dist == float("inf"):
            self.res_label.configure(text=f"Distance: {dist}")
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

        tour = (
            "-".join([str(x["from"]) for x in self._selected_edge])
            + "-"
            + str(self._selected_edge[-1]["to"])
        )

        self.res_label.configure(text=f"Distance: {dist}\nPath: {tour}")
