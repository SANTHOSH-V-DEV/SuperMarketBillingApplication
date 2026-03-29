"""
utils.py — SuperMart
Theme: Raspberry & Shades of Blue
"""

import tkinter as tk
from tkinter import ttk
import uuid
from datetime import datetime

# ── Raspberry & Blue Color Palette ───────────────────────────────────────────
COLORS = {
    "bg":           "#0D0A1A",   # Very deep navy-black
    "surface":      "#1A1030",   # Deep blue-purple surface
    "surface2":     "#241545",   # Mid blue-purple
    "border":       "#3D2060",   # Purple-blue border
    "raspberry":    "#C2185B",   # Primary raspberry
    "raspberry2":   "#E91E8C",   # Bright raspberry accent
    "raspberry_dk": "#880E4F",   # Dark raspberry
    "blue":         "#1565C0",   # Deep blue
    "blue2":        "#1E88E5",   # Medium blue
    "blue3":        "#42A5F5",   # Light blue accent
    "blue_lt":      "#90CAF9",   # Pale blue
    "success":      "#00E676",   # Green
    "warning":      "#FFD740",   # Amber
    "danger":       "#FF1744",   # Red
    "text":         "#F3E5F5",   # Soft white with purple tint
    "text_dim":     "#B39DDB",   # Muted lavender
    "text_muted":   "#6A4FA3",   # Dark lavender
    "odd":          "#150D2B",
    "even":         "#110929",
}


FONTS = {
    "title":   ("Georgia", 24, "bold"),
    "heading": ("Georgia", 14, "bold"),
    "sub":     ("Courier New", 11, "bold"),
    "body":    ("Courier New", 10),
    "small":   ("Courier New", 9),
    "mono":    ("Courier New", 11),
    "label":   ("Helvetica", 10),
    "label_b": ("Helvetica", 10, "bold"),
    "btn":     ("Helvetica", 10, "bold"),
    "big":     ("Georgia", 30, "bold"),
}


def apply_theme(root):
    root.configure(bg=COLORS["bg"])
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(".",
        background=COLORS["bg"],
        foreground=COLORS["text"],
        fieldbackground=COLORS["surface2"],
        bordercolor=COLORS["border"],
        troughcolor=COLORS["surface"],
        selectbackground=COLORS["raspberry"],
        selectforeground="#fff",
        font=FONTS["body"],
    )

    style.configure("TFrame", background=COLORS["bg"])
    style.configure("Card.TFrame", background=COLORS["surface"], relief="flat")
    style.configure("Inner.TFrame", background=COLORS["surface2"])

    style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"])
    style.configure("Card.TLabel", background=COLORS["surface"], foreground=COLORS["text"])
    style.configure("Dim.TLabel", background=COLORS["bg"], foreground=COLORS["text_dim"])
    style.configure("Dim2.TLabel", background=COLORS["surface"], foreground=COLORS["text_dim"])
    style.configure("Title.TLabel", background=COLORS["bg"], foreground=COLORS["text"],
                    font=FONTS["title"])
    style.configure("Heading.TLabel", background=COLORS["surface"], foreground=COLORS["text"],
                    font=FONTS["heading"])
    style.configure("Accent.TLabel", background=COLORS["surface"],
                    foreground=COLORS["raspberry2"], font=FONTS["heading"])
    style.configure("Blue.TLabel", background=COLORS["surface"],
                    foreground=COLORS["blue3"], font=FONTS["heading"])
    style.configure("Success.TLabel", background=COLORS["surface"], foreground=COLORS["success"])
    style.configure("Danger.TLabel", background=COLORS["surface"], foreground=COLORS["danger"])
    style.configure("Warning.TLabel", background=COLORS["surface"], foreground=COLORS["warning"])
    style.configure("Mono.TLabel", background=COLORS["surface"], foreground=COLORS["text"],
                    font=FONTS["mono"])

    style.configure("TEntry",
        fieldbackground=COLORS["surface2"],
        foreground=COLORS["text"],
        insertcolor=COLORS["raspberry2"],
        bordercolor=COLORS["border"],
        relief="flat", padding=6,
    )
    style.map("TEntry", bordercolor=[("focus", COLORS["raspberry2"])])

    style.configure("TCombobox",
        fieldbackground=COLORS["surface2"],
        background=COLORS["surface2"],
        foreground=COLORS["text"],
        arrowcolor=COLORS["text_dim"],
        bordercolor=COLORS["border"],
        relief="flat", padding=5,
    )
    style.map("TCombobox",
        fieldbackground=[("readonly", COLORS["surface2"])],
        foreground=[("readonly", COLORS["text"])],
    )

    # Buttons — Raspberry primary, Blue secondary
    for name, bg, fg, hover in [
        ("Primary",  COLORS["raspberry"],    "#fff", COLORS["raspberry2"]),
        ("Blue",     COLORS["blue"],         "#fff", COLORS["blue2"]),
        ("Success",  "#00897B",              "#fff", "#00695C"),
        ("Danger",   COLORS["danger"],       "#fff", "#D50000"),
        ("Warning",  COLORS["warning"],      "#000", "#FFC400"),
        ("Ghost",    COLORS["surface2"],     COLORS["text"], COLORS["border"]),
        ("DkRasp",   COLORS["raspberry_dk"], "#fff", COLORS["raspberry"]),
    ]:
        style.configure(f"{name}.TButton",
            background=bg, foreground=fg,
            font=FONTS["btn"], relief="flat",
            padding=(14, 8), borderwidth=0,
        )
        style.map(f"{name}.TButton",
            background=[("active", hover), ("pressed", hover)],
            relief=[("pressed", "flat")],
        )

    style.configure("Treeview",
        background=COLORS["even"],
        foreground=COLORS["text"],
        fieldbackground=COLORS["even"],
        rowheight=30,
        borderwidth=0,
        font=FONTS["body"],
    )
    style.configure("Treeview.Heading",
        background=COLORS["surface2"],
        foreground=COLORS["blue_lt"],
        font=FONTS["label_b"],
        relief="flat", borderwidth=0,
    )
    style.map("Treeview",
        background=[("selected", COLORS["raspberry"])],
        foreground=[("selected", "#fff")],
    )

    style.configure("TNotebook", background=COLORS["surface"], borderwidth=0)
    style.configure("TNotebook.Tab",
        background=COLORS["surface2"], foreground=COLORS["text_dim"],
        font=FONTS["label_b"], padding=(18, 8),
    )
    style.map("TNotebook.Tab",
        background=[("selected", COLORS["raspberry_dk"])],
        foreground=[("selected", "#fff")],
    )

    style.configure("TScrollbar",
        background=COLORS["surface2"], troughcolor=COLORS["surface"],
        arrowcolor=COLORS["text_dim"], borderwidth=0,
    )
    style.configure("TSeparator", background=COLORS["raspberry_dk"])

    style.configure("TSpinbox",
        fieldbackground=COLORS["surface2"],
        foreground=COLORS["text"],
        insertcolor=COLORS["raspberry2"],
        arrowcolor=COLORS["text_dim"],
        bordercolor=COLORS["border"],
        relief="flat", padding=5,
    )


def section_header(parent, text, bg=None):
    bg = bg or COLORS["surface"]
    f = tk.Frame(parent, bg=bg)
    tk.Label(f, text=text, font=FONTS["sub"],
             fg=COLORS["raspberry2"], bg=bg).pack(side="left")
    tk.Frame(f, bg=COLORS["raspberry_dk"], height=1).pack(
        side="left", fill="x", expand=True, padx=(10, 0), pady=7)
    return f


def scrollable_tree(parent, columns, headings, show="headings", height=10):
    frame = ttk.Frame(parent)
    tree = ttk.Treeview(frame, columns=columns, show=show, height=height)
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)
    for col, head in zip(columns, headings):
        tree.heading(col, text=head)
    tree.tag_configure("odd",  background=COLORS["odd"])
    tree.tag_configure("even", background=COLORS["even"])
    return frame, tree


def tree_reload(tree, rows, cols):
    for item in tree.get_children():
        tree.delete(item)
    for i, row in enumerate(rows):
        tag = "odd" if i % 2 else "even"
        tree.insert("", "end", values=[row[c] for c in cols], tags=(tag,))


def generate_bill_id():
    return "BL-" + uuid.uuid4().hex[:8].upper()


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def currency(amount):
    return f"₹{amount:,.2f}"


def show_toast(root, message, kind="success", duration=2500):
    colors = {
        "success": (COLORS["success"],    "#000"),
        "error":   (COLORS["danger"],     "#fff"),
        "info":    (COLORS["blue2"],      "#fff"),
        "warning": (COLORS["warning"],    "#000"),
        "rasp":    (COLORS["raspberry2"], "#fff"),
    }
    bg, fg = colors.get(kind, colors["info"])
    toast = tk.Toplevel(root)
    toast.overrideredirect(True)
    toast.attributes("-topmost", True)
    toast.configure(bg=bg)
    tk.Label(toast, text=message, bg=bg, fg=fg,
             font=FONTS["label_b"], padx=22, pady=12).pack()
    root.update_idletasks()
    w, h = toast.winfo_reqwidth(), toast.winfo_reqheight()
    x = root.winfo_x() + (root.winfo_width()  - w) // 2
    y = root.winfo_y() +  root.winfo_height() - h - 30
    toast.geometry(f"+{x}+{y}")
    toast.after(duration, toast.destroy)


# Product emoji icons (used as visual stand-ins for images)
PRODUCT_ICONS = {
    "rice":      "🌾",
    "wheat":     "🌾",
    "flour":     "🌾",
    "sugar":     "🍬",
    "salt":      "🧂",
    "oil":       "🫙",
    "cooking":   "🫙",
    "milk":      "🥛",
    "bread":     "🍞",
    "egg":       "🥚",
    "butter":    "🧈",
    "tea":       "🍵",
    "coffee":    "☕",
    "biscuit":   "🍪",
    "chocolate": "🍫",
    "juice":     "🧃",
    "water":     "💧",
    "soap":      "🧼",
    "shampoo":   "🧴",
    "default":   "📦",
}


def get_product_icon(name):
    """Return an emoji icon based on product name keywords."""
    name_lower = name.lower()
    for keyword, icon in PRODUCT_ICONS.items():
        if keyword in name_lower:
            return icon
    return PRODUCT_ICONS["default"]
