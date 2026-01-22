"""
Simple On-Screen Keyboard with manual language selection
No external dependencies except tkinter (built-in with Python)
"""

import tkinter as tk
from tkinter import ttk

# ─── Layout Definitions ──────────────────────────────────────────────────────

QWERTY_EN = [
    ['`~', '1!', '2@', '3#', '4$', '5%', '6^', '7&', '8*', '9(', '0)', '-_', '=+', '⌫'],
    ['Tab', 'qQ', 'wW', 'eE', 'rR', 'tT', 'yY', 'uU', 'iI', 'oO', 'pP', '[{', ']}', '\\|'],
    ['CapsLock', 'aA', 'sS', 'dD', 'fF', 'gG', 'hH', 'jJ', 'kK', 'lL', ';:', '\'"', '⏎'],
    ['Shift', 'zZ', 'xX', 'cC', 'vV', 'bB', 'nN', 'mM', ',<', '.>', '/?', 'Shift'],
    ['Space                                 ']
]

AZERTY_FR = [
    ['²~', '&1', 'é2~', '"3#', "'4{", '(5[', '-6|', 'è7`', '_8\\', 'ç9^', 'à0@', ')°]', '=+} ', '⌫'],
    ['Tab', 'aA', 'zZ', 'eE€', 'rR', 'tT', 'yY', 'uU', 'iI', 'oO', 'pP', '^¨', '$£', '\\*'],
    ['CapsLock', 'qQ', 'sS', 'dD', 'fF', 'gG', 'hH', 'jJ', 'kK', 'lL', 'mM', 'ù%', '⏎'],
    ['Shift', '<>', 'wW', 'xX', 'cC', 'vV', 'bB', 'nN', ',?', ';.', ':!', 'Shift'],
    ['Space                                 ']
]

UKRAINIAN_JCUKEN = [
    ['ґ~', '1!', '2"', '3№', '4;', '5%', '6:', '7?', '8*', '9(', '0)', '-_', '=+', '⌫'],
    ['Tab', 'йЙ', 'цЦ', 'уУ', 'кК', 'еЕ', 'нН', 'гГ', 'шШ', 'щЩ', 'зЗ', 'хХ', 'їЇ', '\\|'],
    ['CapsLock', 'фФ', 'іІ', 'вВ', 'аА', 'пП', 'рР', 'оО', 'лЛ', 'дД', 'жЖ', 'єЄ', '⏎'],
    ['Shift', 'яЯ', 'чЧ', 'сС', 'мМ', 'иИ', 'тТ', 'ьЬ', 'бБ', 'юЮ', '.,', 'Shift'],
    ['Space                                 ']
]

LAYOUTS = {
    "English (QWERTY)": QWERTY_EN,
    "Français (AZERTY)": AZERTY_FR,
    "Українська (ЙЦУКЕН)": UKRAINIAN_JCUKEN
}


class OnScreenKeyboard:
    def __init__(self, master, target_entry=None):
        self.master = master
        self.target_entry = target_entry
        self.window = None
        self.buttons = []
        self.shift_active = False
        self.current_layout_name = "English (QWERTY)"
        self.current_layout_keys = LAYOUTS[self.current_layout_name]

        self._create_keyboard_window()
        self._build_keyboard()

    def _create_keyboard_window(self):
        self.window = tk.Toplevel(self.master)
        self.window.title("Virtual Keyboard")
        self.window.resizable(False, False)
        self.window.attributes("-topmost", True)

        w = 880
        h = 420
        x = self.master.winfo_screenwidth() // 2 - w // 2
        y = self.master.winfo_screenheight() - h - 100
        self.window.geometry(f"{w}x{h}+{x}+{y}")

    def _build_keyboard(self):
        # Clear everything
        for widget in self.window.winfo_children():
            widget.destroy()
        self.buttons.clear()

        # Language selector
        tk.Label(self.window, text="Language:", font=("Segoe UI", 10)).pack(pady=6)

        lang_var = tk.StringVar(value=self.current_layout_name)
        lang_menu = ttk.OptionMenu(
            self.window, lang_var,
            self.current_layout_name,
            *LAYOUTS.keys(),
            command=self._change_language
        )
        lang_menu.pack(pady=4)

        # Keyboard frame
        kb_frame = tk.Frame(self.window)
        kb_frame.pack(pady=10, padx=10, fill="both", expand=True)

        for row_idx, row in enumerate(self.current_layout_keys):
            for col_idx, key_pair in enumerate(row):
                if not key_pair.strip():
                    continue

                display = key_pair[0]  # unshifted

                if "Space" in key_pair:
                    btn = ttk.Button(
                        kb_frame, text="Space", width=55,
                        command=lambda: self._press(" ")
                    )
                    btn.grid(row=row_idx, column=col_idx, columnspan=14,
                             padx=4, pady=6, sticky="ew")
                else:
                    width = 5 if len(key_pair) <= 2 else 7
                    btn = ttk.Button(
                        kb_frame, text=display, width=width,
                        command=lambda k=key_pair: self._press(k)
                    )
                    btn.grid(row=row_idx, column=col_idx,
                             padx=3, pady=5, sticky="nsew")

                self.buttons.append(btn)

        # Grid config
        for i in range(15):
            kb_frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            kb_frame.grid_rowconfigure(i, weight=1)

        self.window.title(f"Virtual Keyboard – {self.current_layout_name}")

    def _change_language(self, selection):
        self.current_layout_name = selection
        self.current_layout_keys = LAYOUTS[selection]
        self.shift_active = False  # reset shift when changing layout
        self._build_keyboard()

    def _toggle_shift(self):
        self.shift_active = not self.shift_active
        for btn in self.buttons:
            current = btn.cget("text")
            for row in self.current_layout_keys:
                for pair in row:
                    if current in pair:
                        new_text = pair[1] if self.shift_active else pair[0]
                        btn.configure(text=new_text)
                        break

    def _press(self, key_pair):
        if not self.target_entry or not self.target_entry.winfo_exists():
            return

        if "⌫" in key_pair:
            current = self.target_entry.get()
            if current:
                self.target_entry.delete(len(current)-1, tk.END)
            return

        if "⏎" in key_pair:
            self.target_entry.insert(tk.END, "\n")
            return

        if "Space" in key_pair:
            self.target_entry.insert(tk.END, " ")
            return

        char = key_pair[1] if self.shift_active and len(key_pair) >= 2 else key_pair[0]
        self.target_entry.insert(tk.END, char)

    def show(self):
        if self.window:
            self.window.deiconify()
            self.window.lift()


# ─── Demo ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    root.title("On-Screen Keyboard Demo")
    root.geometry("800x500")

    style = ttk.Style()
    style.configure("TButton", font=("Segoe UI", 12), padding=6)

    entry = ttk.Entry(root, font=("Segoe UI", 16), width=50)
    entry.pack(pady=60)
    entry.focus_set()

    keyboard = OnScreenKeyboard(root, target_entry=entry)

    def on_focus(event):
        keyboard.show()

    entry.bind("<FocusIn>", on_focus)

    root.mainloop()
