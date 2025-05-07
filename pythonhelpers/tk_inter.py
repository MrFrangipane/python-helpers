from tkinter import ttk
import tkinter as tk


class Widget:
    Width = 300
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
    _ValueClass = tk.DoubleVar

    def __init__(self, caption, parent: Widget, on_change, range_=None, is_range_symmetric=False, min_=0, max_=None):
        super().__init__()
        self._on_change = on_change
        self._caption = caption
        self._label = ttk.Label(parent.tk_class(), text=caption)
        self._label.pack(pady=Slider.Padding)

        self.value = self._ValueClass()
        self._tk_class = ttk.Scale(
            parent.tk_class(),
            from_=-range_ if (range_ is not None and is_range_symmetric) else min_,
            to=range_ if max_ is None else max_,
            length=Slider.Width,
            command=self._changed,
            variable=self.value,
        )
        self._tk_class.pack(pady=Slider.Padding)

    def _changed(self, value):
        value = float(value)
        self._label.config(text=f'{self._caption}: {value:.2f}')
        self._on_change(value)

    def get(self):
        return self.value.get()

    def set(self, value):
        value = float(value)
        self._label.config(text=f'{self._caption}: {value:.2f}')
        self.value.set(value)


class IntegerSlider(Slider):
    _ValueClass = tk.IntVar

    def _changed(self, value):
        value = int(float(value))
        self._label.config(text=f'{self._caption}: {value}')
        self._on_change(value)

    def get(self):
        return self.value.get()

    def set(self, value):
        value = int(float(value))
        self._label.config(text=f'{self._caption}: {value}')
        self.value.set(value)


class Button(Widget):
    def __init__(self, caption: str, parent: Widget, on_press, on_release=None):
        super().__init__()
        self._on_pressed = on_press
        self._on_release = on_release
        self._tk_class = ttk.Button(
            parent.tk_class(),
            text=caption
        )
        self._tk_class.bind('<ButtonPress-1>', self._pressed)
        self._tk_class.bind('<ButtonRelease-1>', self._released)

        self._tk_class.pack(pady=Button.Padding)
        self.is_pressed = False

    def _pressed(self, _):
        self.is_pressed = True
        self._on_pressed(_)

    def _released(self, _):
        self.is_pressed = False
        if self._on_release is not None:
            self._on_release(_)


class CheckBox(Widget):
    def __init__(self, caption: str, parent: Widget, on_on, on_off=None):
        super().__init__()
        self._value = tk.BooleanVar()
        self._on_on = on_on
        self._on_off = on_off
        self._tk_class = ttk.Checkbutton(
            parent.tk_class(),
            text=caption,
            variable=self._value,
            command=self._toggled
        )
        self._tk_class.pack(pady=Button.Padding)
        self.is_pressed = False

    def _toggled(self):
        if self.checked():
            self._on_on(True)
        else:
            self._on_off(False)

    def checked(self):
        return self._value.get()

    def set(self, is_checked: bool):
        self._value.set(is_checked)
