import tkinter as tk
import subprocess
import sys

LETTERS = [
    ('Α', 'α', 'alpha'),   ('Β', 'β', 'beta'),    ('Γ', 'γ', 'gamma'),
    ('Δ', 'δ', 'delta'),   ('Ε', 'ε', 'epsilon'), ('Ζ', 'ζ', 'zeta'),
    ('Η', 'η', 'eta'),     ('Θ', 'θ', 'theta'),   ('Ι', 'ι', 'iota'),
    ('Κ', 'κ', 'kappa'),   ('Λ', 'λ', 'lambda'),  ('Μ', 'μ', 'mu'),
    ('Ν', 'ν', 'nu'),      ('Ξ', 'ξ', 'xi'),      ('Ο', 'ο', 'omicron'),
    ('Π', 'π', 'pi'),      ('Ρ', 'ρ', 'rho'),     ('Σ', 'σ', 'sigma'),
    ('Τ', 'τ', 'tau'),     ('Υ', 'υ', 'upsilon'), ('Φ', 'φ', 'phi'),
    ('Χ', 'χ', 'chi'),     ('Ψ', 'ψ', 'psi'),     ('Ω', 'ω', 'omega'),
]

def copy_to_clipboard(text):
    """Copie via pbcopy (plus fiable que tkinter sur macOS)."""
    subprocess.run(['pbcopy'], input=text.encode('utf-8'), check=False)

class GreekPicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Greek")
        self.root.configure(bg='#1e1e1e')

        self.root.attributes('-topmost', True)

        screen_w = self.root.winfo_screenwidth()
        win_w, win_h = 360, 280
        x = screen_w - win_w - 30
        y = 80
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")

        self.root.bind('<Escape>', lambda e: self.root.destroy())

        self.status_var = tk.StringVar(value="Cliquer une lettre pour la copier")
        status = tk.Label(
            self.root, textvariable=self.status_var,
            bg='#1e1e1e', fg='#888', font=('SF Pro Text', 11), pady=6
        )
        status.pack(fill='x')

        grid_frame = tk.Frame(self.root, bg='#1e1e1e')
        grid_frame.pack(padx=8, pady=4, fill='both', expand=True)

        for i, (upper, lower, name) in enumerate(LETTERS):
            row, col = i // 6, i % 6
            btn = self._make_button(grid_frame, upper, lower, name)
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')

        for c in range(6):
            grid_frame.columnconfigure(c, weight=1)
        for r in range(4):
            grid_frame.rowconfigure(r, weight=1)

        self.root.focus_force()

    def _make_button(self, parent, upper, lower, name):
        frame = tk.Frame(parent, bg='#2a2a2a', cursor='hand2')
        label_letters = tk.Label(
            frame, text=f"{upper} {lower}",
            bg='#2a2a2a', fg='#fff', font=('SF Pro Display', 14)
        )
        label_name = tk.Label(
            frame, text=name,
            bg='#2a2a2a', fg='#777', font=('SF Pro Text', 9)
        )
        label_letters.pack(pady=(4, 0))
        label_name.pack(pady=(0, 4))

        def on_click(event=None):
            copy_to_clipboard(lower)
            self.status_var.set(f"« {lower} » copié — ⌘V pour coller")

            frame.configure(bg='#3a5a3a')
            label_letters.configure(bg='#3a5a3a')
            label_name.configure(bg='#3a5a3a')
            self.root.after(150, lambda: self._reset_bg(frame, label_letters, label_name))

        def on_right_click(event=None):
            """Clic droit = copie la majuscule."""
            copy_to_clipboard(upper)
            self.status_var.set(f"« {upper} » copié — ⌘V pour coller")
            frame.configure(bg='#3a5a3a')
            label_letters.configure(bg='#3a5a3a')
            label_name.configure(bg='#3a5a3a')
            self.root.after(150, lambda: self._reset_bg(frame, label_letters, label_name))

        for w in (frame, label_letters, label_name):
            w.bind('<Button-1>', on_click)
            w.bind('<Button-2>', on_right_click)
            w.bind('<Button-3>', on_right_click)
            w.bind('<Enter>', lambda e, f=frame, l1=label_letters, l2=label_name: self._hover(f, l1, l2, True))
            w.bind('<Leave>', lambda e, f=frame, l1=label_letters, l2=label_name: self._hover(f, l1, l2, False))

        return frame

    def _hover(self, frame, l1, l2, entering):
        color = '#3a3a3a' if entering else '#2a2a2a'
        frame.configure(bg=color)
        l1.configure(bg=color)
        l2.configure(bg=color)

    def _reset_bg(self, frame, l1, l2):
        frame.configure(bg='#2a2a2a')
        l1.configure(bg='#2a2a2a')
        l2.configure(bg='#2a2a2a')

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    GreekPicker().run()
