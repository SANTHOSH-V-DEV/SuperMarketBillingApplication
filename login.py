"""
login.py — SuperMart Login Screen
Theme: Supermarket background image with frosted glass card
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import database as db
import utils as u

# Path to background image (sits next to login.py)
BG_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "bg_login.jpg")


class LoginScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SuperMart — Login")
        self.configure(bg=u.COLORS["bg"])
        u.apply_theme(self)
        self._bg_photo = None

        # ── Maximise window ───────────────────────────────────────────────────
        try:
            self.state("zoomed")           # Windows
        except tk.TclError:
            w = self.winfo_screenwidth()
            h = self.winfo_screenheight()
            self.geometry(f"{w}x{h}+0+0")

        self._build()
        # Re-draw background whenever window is resized
        self.bind("<Configure>", self._on_resize)

    # ── Build UI ──────────────────────────────────────────────────────────────

    def _build(self):
        C = u.COLORS

        # ── Full-screen canvas (background layer) ─────────────────────────────
        self.bg_canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Draw background image (or solid colour fallback)
        self._draw_background()

        # ── Raspberry top strip ───────────────────────────────────────────────
        top_strip = tk.Frame(self, bg=C["raspberry"], height=6)
        top_strip.place(x=0, y=0, relwidth=1)

        # ── Blue bottom strip ─────────────────────────────────────────────────
        bottom_strip = tk.Frame(self, bg=C["blue"], height=4)
        bottom_strip.place(x=0, rely=1.0, y=-4, relwidth=1)

        # ── Centered login card ───────────────────────────────────────────────
        # Use a real Frame placed dead-centre via place()
        self.card_outer = tk.Frame(
            self,
            bg="#12082A",                       # deep translucent navy
            highlightbackground=C["raspberry"],
            highlightthickness=2,
        )
        self.card_outer.place(relx=0.5, rely=0.5, anchor="center")

        self._build_card(self.card_outer)

    # ── Background image ──────────────────────────────────────────────────────

    def _draw_background(self):
        """Draw the background image scaled to the current window size."""
        try:
            from PIL import Image, ImageTk
            w = self.winfo_screenwidth()
            h = self.winfo_screenheight()
            img = Image.open(BG_IMAGE_PATH).resize((w, h), Image.LANCZOS)
            self._bg_photo = ImageTk.PhotoImage(img)
            self.bg_canvas.delete("bg")
            self.bg_canvas.create_image(
                0, 0, anchor="nw",
                image=self._bg_photo, tags="bg")
        except Exception:
            # PIL not installed or image missing — use a gradient-like solid bg
            self.bg_canvas.configure(bg=u.COLORS["bg"])

    def _on_resize(self, event):
        # Only redraw if the root window itself changed size
        if event.widget is self:
            self._draw_background()

    # ── Card content ──────────────────────────────────────────────────────────

    def _build_card(self, parent):
        C = u.COLORS

        # Raspberry top accent bar on card
        tk.Frame(parent, bg=C["raspberry"], height=4).pack(fill="x")

        inner = tk.Frame(parent, bg="#12082A")
        inner.pack(padx=44, pady=32)

        # ── Logo section ──────────────────────────────────────────────────────
        logo_f = tk.Frame(inner, bg="#12082A")
        logo_f.pack(pady=(0, 20))

        # Cart icon bubble
        bubble = tk.Frame(logo_f, bg=C["raspberry"], width=68, height=68)
        bubble.pack()
        bubble.pack_propagate(False)
        tk.Label(bubble, text="🛒", font=("Helvetica", 30),
                 bg=C["raspberry"], fg="#fff").pack(expand=True)

        tk.Label(logo_f, text="SuperMart",
                 font=("Georgia", 26, "bold"),
                 bg="#12082A", fg="#FFFFFF").pack(pady=(8, 2))

        # Teal underline (picks up the teal tones from the bg image)
        tk.Frame(logo_f, bg="#26C6DA", height=3, width=110).pack()

        tk.Label(logo_f, text="Point of Sale System",
                 font=u.FONTS["small"], bg="#12082A",
                 fg="#90CAF9").pack(pady=(5, 0))

        # ── Divider ───────────────────────────────────────────────────────────
        tk.Frame(inner, bg=C["raspberry_dk"], height=1).pack(
            fill="x", pady=(0, 16))

        tk.Label(inner, text="SIGN IN", font=u.FONTS["sub"],
                 bg="#12082A", fg=C["raspberry2"]).pack(anchor="w", pady=(0, 12))

        # ── Username ──────────────────────────────────────────────────────────
        tk.Label(inner, text="Username", font=u.FONTS["label"],
                 bg="#12082A", fg="#B0BEC5").pack(anchor="w")
        self.username_var = tk.StringVar()
        user_entry = ttk.Entry(inner, textvariable=self.username_var, width=36)
        user_entry.pack(fill="x", pady=(3, 10), ipady=5)

        # ── Password ──────────────────────────────────────────────────────────
        tk.Label(inner, text="Password", font=u.FONTS["label"],
                 bg="#12082A", fg="#B0BEC5").pack(anchor="w")
        self.password_var = tk.StringVar()
        self.pass_entry = ttk.Entry(
            inner, textvariable=self.password_var, show="●", width=36)
        self.pass_entry.pack(fill="x", pady=(3, 6), ipady=5)

        # Show password toggle
        self.show_pw = tk.BooleanVar(value=False)
        tk.Checkbutton(
            inner, text="Show password",
            variable=self.show_pw,
            command=self._toggle_pw,
            bg="#12082A", fg="#90CAF9",
            activebackground="#12082A",
            selectcolor="#1A1030",
            font=u.FONTS["small"],
            relief="flat", bd=0,
        ).pack(anchor="w", pady=(0, 10))

        # ── Role selection ────────────────────────────────────────────────────
        tk.Frame(inner, bg=C["border"], height=1).pack(fill="x", pady=(0, 10))

        self.role_var = tk.StringVar(value="user")

        role_frame = tk.Frame(inner, bg="#12082A")
        role_frame.pack(fill="x", pady=(0, 16))

        tk.Label(role_frame, text="Login As:",
                 font=u.FONTS["label"],
                 bg="#12082A", fg="#B0BEC5").pack(side="left", padx=(0, 12))

        for role, icon in [("User", "👤"), ("Admin", "🔑")]:
            rb_frame = tk.Frame(role_frame, bg="#12082A")
            rb_frame.pack(side="left", padx=(0, 10))
            tk.Radiobutton(
                rb_frame,
                text=f"{icon} {role}",
                variable=self.role_var,
                value=role.lower(),
                bg="#12082A", fg="#fff",
                activebackground="#12082A",
                selectcolor=C["raspberry_dk"],
                font=u.FONTS["label"],
                relief="flat", cursor="hand2",
            ).pack()

        # ── Login button ──────────────────────────────────────────────────────
        login_btn = tk.Button(
            inner,
            text="LOGIN  →",
            font=("Helvetica", 11, "bold"),
            bg=C["raspberry"],
            fg="#ffffff",
            activebackground=C["raspberry2"],
            activeforeground="#ffffff",
            relief="flat", bd=0,
            cursor="hand2",
            command=self._login,
            pady=11,
        )
        login_btn.pack(fill="x")
        login_btn.bind("<Enter>",
            lambda e: login_btn.config(bg=C["raspberry2"]))
        login_btn.bind("<Leave>",
            lambda e: login_btn.config(bg=C["raspberry"]))

        # ── Helper text ───────────────────────────────────────────────────────
        tk.Frame(inner, bg=C["border"], height=1).pack(fill="x", pady=(14, 8))
        tk.Label(inner,
                 text="Please select your role before logging in.",
                 font=u.FONTS["small"],
                 bg="#12082A", fg="#546E7A").pack()

        # Bind Enter key & focus
        self.bind("<Return>", lambda e: self._login())
        user_entry.focus()

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _toggle_pw(self):
        self.pass_entry.config(show="" if self.show_pw.get() else "●")

    def _login(self):
        username      = self.username_var.get().strip()
        password      = self.password_var.get().strip()
        selected_role = self.role_var.get()

        if not username or not password:
            messagebox.showwarning("Missing Fields",
                "Please enter both username and password.")
            return

        user = db.get_user(username, password)
        if user is None:
            messagebox.showerror("Login Failed",
                "Invalid username or password.")
            return

        actual_role = user.get("role", "").lower()
        if actual_role != selected_role:
            messagebox.showerror("Access Denied",
                f"This account does not have '{selected_role}' privileges.")
            return

        self.destroy()
        if actual_role == "admin":
            from admin import AdminPanel
            AdminPanel(user).mainloop()
        else:
            from billing import BillingScreen
            BillingScreen(user).mainloop()
