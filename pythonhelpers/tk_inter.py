from tkinter import ttk
import tkinter as tk


class Widget:
    Width = 200
    Padding = 5

    def __init__(self):
        self._tk_class = None

    def tk_class(self):
        return self._tk_class


class Main(Widget):
    def __init__(self, caption):
        super().__init__()
        self._tk_class = tk.Tk()
        self._tk_class.title(caption)

    @staticmethod
    def run():
        tk.mainloop()


class Frame(Widget):
    def __init__(self, caption: str, parent: Widget, grid_row: int, grid_column: int):
        super().__init__()
        self._tk_class = ttk.Frame(
            parent.tk_class(),
            borderwidth=2
        )
        self._tk_class.grid(
            row=grid_row,
            column=grid_column,
            padx=Frame.Padding,
            pady=Frame.Padding
        )
        self.label = ttk.Label(
            self._tk_class,
            text=caption
        )
        self.label.pack(
            pady=Frame.Padding
        )


class Slider(Widget):
    def __init__(self, caption, parent: Widget, command, range_=None, is_range_symmetric=False, min_=0, max_=None):
        super().__init__()
        self.label = ttk.Label(parent.tk_class(), text=caption)
        self.label.pack(pady=Slider.Padding)

        self.value = tk.IntVar()
        self._tk_class = ttk.Scale(
            parent.tk_class(),
            from_=-range_ if (range_ is not None and is_range_symmetric) else min_,
            to=range_ if max_ is None else max_,
            length=Slider.Width,
            command=command,
            variable=self.value,
        )
        self._tk_class.pack(pady=Slider.Padding)

    def get(self):
        return self.value.get()

    def set(self, value):
        self.value.set(value)


class Button(Widget):
    def __init__(self, caption: str, parent: Widget, command):
        super().__init__()
        self._tk_class = ttk.Button(
            parent.tk_class(),
            text=caption,
            command=command
        )
        self._tk_class.pack(pady=Button.Padding)
