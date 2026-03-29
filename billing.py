"""
billing.py — SuperMart Billing Screen
Features: Product grid card selection with real images, full-screen layout, anchored layout, PDF receipts
Theme: Raspberry & Shades of Blue
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import database as db
import utils as u

# ── Images are stored in a folder next to the app ────────────────────────────
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "product_images")
os.makedirs(IMAGES_DIR, exist_ok=True)

def _get_product_image_path(product_name):
    """Return the saved image path for a product, or None if not set."""
    safe_name = "".join(
        c if c.isalnum() or c in (" ", "_") else "_"
        for c in product_name
    ).strip().replace(" ", "_")
    for ext in (".png", ".jpg", ".jpeg", ".gif", ".bmp"):
        path = os.path.join(IMAGES_DIR, safe_name + ext)
        if os.path.exists(path):
            return path
    return None

def _load_tk_image(path, size=(100, 90)):
    """Load an image using PIL if available, else return None."""
    try:
        from PIL import Image, ImageTk
        img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except ImportError:
        return None
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

class BillingScreen(tk.Tk):
    def __init__(self, user, parent_admin=None):
        super().__init__()
        self.user         = user
        self.parent_admin = parent_admin
        self.cart         = []
        self.bill_id      = u.generate_bill_id()
        self._selected_product = None   
        self._photo_refs = []           

        self.title(f"SuperMart — Billing  [{user['username']}]")
        self.configure(bg=u.COLORS["bg"])
        u.apply_theme(self)
        
        # Maximize the window natively
        try:
            self.state('zoomed') 
        except tk.TclError:
            w, h = self.winfo_screenwidth(), self.winfo_screenheight()
            self.geometry(f"{w}x{h}+0+0")

        self._build()
        self._refresh_products()

    # ── Main Layout ───────────────────────────────────────────────────────────

    def _build(self):
        self._topbar()
        body = tk.Frame(self, bg=u.COLORS["bg"])
        body.pack(fill="both", expand=True, padx=10, pady=(8, 10))

        # LEFT — product grid
        left = tk.Frame(body, bg=u.COLORS["bg"])
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))

        # RIGHT — cart + checkout (fixed width)
        right = tk.Frame(body, bg=u.COLORS["bg"])
        right.pack(side="right", fill="both", padx=(6, 0))
        right.config(width=420)
        right.pack_propagate(False)

        self._build_product_section(left)
        self._build_cart_section(right)

    def _topbar(self):
        C = u.COLORS
        bar = tk.Frame(self, bg=C["raspberry_dk"], height=54)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(bar, text="🛒  SuperMart", font=u.FONTS["heading"],
                 bg=C["raspberry_dk"], fg="#fff").pack(side="left", padx=16)
        tk.Frame(bar, bg=C["raspberry"], width=2).pack(
            side="left", fill="y", pady=10, padx=8)

        self._bill_lbl = tk.Label(
            bar, text=f"Bill: {self.bill_id}",
            font=u.FONTS["small"],
            bg=C["raspberry_dk"], fg=C["blue_lt"])
        self._bill_lbl.pack(side="left", padx=6)

        right_bar = tk.Frame(bar, bg=C["raspberry_dk"])
        right_bar.pack(side="right", padx=12, fill="y")

        tk.Label(right_bar, text=f"👤 {self.user['username']}",
                 font=u.FONTS["small"], bg=C["raspberry_dk"],
                 fg=C["blue_lt"]).pack(side="left", padx=8)

        if self.user.get("role", "").lower() == "admin":
            tk.Button(right_bar, text="Admin Panel",
                      font=u.FONTS["btn"],
                      bg=C["blue"], fg="#fff",
                      relief="flat", bd=0, cursor="hand2",
                      padx=10, pady=4,
                      command=self._go_admin).pack(side="left", padx=4)

        tk.Button(right_bar, text="Logout",
                  font=u.FONTS["btn"],
                  bg=C["surface2"], fg=C["text"],
                  relief="flat", bd=0, cursor="hand2",
                  padx=10, pady=4,
                  command=self._logout).pack(side="left", padx=4)

    # ── Product Section (LEFT) ────────────────────────────────────────────────

    def _build_product_section(self, parent):
        C = u.COLORS

        # ── Customer details ──────────────────────────────────────────────────
        cust = tk.Frame(parent, bg=C["surface"],
                        highlightbackground=C["raspberry_dk"],
                        highlightthickness=1)
        cust.pack(fill="x", pady=(0, 8))
        tk.Frame(cust, bg=C["raspberry"], height=3).pack(fill="x")

        ci = tk.Frame(cust, bg=C["surface"])
        ci.pack(fill="x", padx=16, pady=8)

        tk.Label(ci, text="CUSTOMER DETAILS", font=u.FONTS["sub"],
                 bg=C["surface"], fg=C["raspberry2"]).grid(
            row=0, column=0, columnspan=5,
            sticky="w", pady=(0, 6))

        self.cust_name  = tk.StringVar()
        self.cust_phone = tk.StringVar()

        tk.Label(ci, text="Name", font=u.FONTS["label"],
                 bg=C["surface"], fg=C["text_dim"]).grid(
            row=1, column=0, sticky="w")
        ttk.Entry(ci, textvariable=self.cust_name, width=22).grid(
            row=1, column=1, sticky="ew",
            padx=(6, 15), ipady=3)

        tk.Label(ci, text="Phone", font=u.FONTS["label"],
                 bg=C["surface"], fg=C["text_dim"]).grid(
            row=1, column=2, sticky="w")
        ttk.Entry(ci, textvariable=self.cust_phone, width=16).grid(
            row=1, column=3, sticky="ew",
            padx=(6, 10), ipady=3)
            
        tk.Button(ci, text="✔ Set Customer", font=u.FONTS["small"],
                  bg=C["blue"], fg="#fff", relief="flat", cursor="hand2",
                  padx=10, pady=2, command=self._set_customer_ui).grid(
            row=1, column=4, sticky="e", padx=(5, 0))

        ci.columnconfigure(1, weight=1)
        ci.columnconfigure(3, weight=1)

        # ── Add-to-cart bar ───────────────────────────────────────────────────
        add_bar = tk.Frame(parent, bg=C["surface"],
                           highlightbackground=C["blue"],
                           highlightthickness=1)
        add_bar.pack(fill="x", pady=(0, 8))
        tk.Frame(add_bar, bg=C["blue"], height=3).pack(fill="x")

        ab = tk.Frame(add_bar, bg=C["surface"])
        ab.pack(fill="x", padx=14, pady=8)

        tk.Label(ab, text="Selected:", font=u.FONTS["label"],
                 bg=C["surface"], fg=C["text_dim"]).pack(side="left")

        self.selected_icon_lbl = tk.Label(
            ab, text="—", font=("Helvetica", 20),
            bg=C["surface"], fg=C["raspberry2"])
        self.selected_icon_lbl.pack(side="left", padx=(8, 4))

        self.selected_name_lbl = tk.Label(
            ab, text="No product selected",
            font=u.FONTS["label_b"],
            bg=C["surface"], fg=C["text"])
        self.selected_name_lbl.pack(side="left", padx=(0, 14))

        self.selected_price_lbl = tk.Label(
            ab, text="",
            font=("Georgia", 13, "bold"),
            bg=C["surface"], fg=C["raspberry2"])
        self.selected_price_lbl.pack(side="left", padx=(0, 20))

        self.selected_stock_lbl = tk.Label(
            ab, text="",
            font=u.FONTS["small"],
            bg=C["surface"], fg=C["text_dim"])
        self.selected_stock_lbl.pack(side="left", padx=(0, 20))

        tk.Label(ab, text="Qty:", font=u.FONTS["label"],
                 bg=C["surface"], fg=C["text_dim"]).pack(side="left")
        self.qty_var = tk.IntVar(value=1)
        ttk.Spinbox(ab, from_=1, to=999,
                    textvariable=self.qty_var,
                    width=5).pack(side="left", padx=(6, 10), ipady=3)

        tk.Button(ab, text="➕  Add to Cart",
                  font=u.FONTS["btn"],
                  bg=C["raspberry"], fg="#fff",
                  relief="flat", bd=0, cursor="hand2",
                  padx=14, pady=5,
                  activebackground=C["raspberry2"],
                  command=self._add_to_cart).pack(side="left")

        # ── Product grid ──────────────────────────────────────────────────────
        grid_hdr = tk.Frame(parent, bg=C["bg"])
        grid_hdr.pack(fill="x", pady=(2, 4))

        tk.Label(grid_hdr,
                 text="SELECT A PRODUCT  — click a card to select it",
                 font=u.FONTS["sub"],
                 bg=C["bg"], fg=C["raspberry2"]).pack(side="left")
        tk.Frame(grid_hdr, bg=C["raspberry_dk"], height=1).pack(
            side="left", fill="x", expand=True,
            padx=(10, 0), pady=7)

        canvas_wrap = tk.Frame(parent, bg=C["bg"])
        canvas_wrap.pack(fill="both", expand=True)

        self.prod_canvas = tk.Canvas(
            canvas_wrap, bg=C["bg"],
            highlightthickness=0, bd=0)
        vsb = ttk.Scrollbar(canvas_wrap, orient="vertical",
                             command=self.prod_canvas.yview)
        self.prod_canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.prod_canvas.pack(side="left", fill="both", expand=True)

        self.prod_grid = tk.Frame(self.prod_canvas, bg=C["bg"])
        self._prod_win = self.prod_canvas.create_window(
            (0, 0), window=self.prod_grid, anchor="nw")

        self.prod_grid.bind("<Configure>",
            lambda e: self.prod_canvas.configure(
                scrollregion=self.prod_canvas.bbox("all")))
        self.prod_canvas.bind("<Configure>",
            lambda e: self.prod_canvas.itemconfig(
                self._prod_win, width=e.width))
        self.prod_canvas.bind("<MouseWheel>",
            lambda e: self.prod_canvas.yview_scroll(
                int(-1*(e.delta/120)), "units"))

        self._card_widgets = {}

    def _set_customer_ui(self):
        name = self.cust_name.get().strip()
        phone = self.cust_phone.get().strip()
        if not name and not phone:
            messagebox.showinfo("Customer", "Please enter a name or phone number first.")
            return
        u.show_toast(self, f"Customer '{name or 'Walk-in'}' attached to current bill.", kind="info")

    # ── Cart Section (RIGHT) ──────────────────────────────────────────────────

    def _build_cart_section(self, parent):
        C = u.COLORS

        # 1. Header (Packed to top)
        hdr = tk.Frame(parent, bg=C["raspberry_dk"])
        hdr.pack(side="top", fill="x", pady=(0, 6))
        tk.Label(hdr, text="🛒  SHOPPING CART",
                 font=u.FONTS["sub"],
                 bg=C["raspberry_dk"], fg="#fff",
                 pady=8, padx=12).pack(side="left")

        # 2. Bottom Wrapper (Anchored to absolute bottom to prevent cut-offs)
        bottom_wrap = tk.Frame(parent, bg=C["bg"])
        bottom_wrap.pack(side="bottom", fill="x")

        # FIXED: Relocated "Remove Selected" to the top of the Bottom Wrapper so it never disappears!
        tk.Button(bottom_wrap, text="🗑  Remove Selected",
                  font=u.FONTS["btn"],
                  bg="#B71C1C", fg="#fff",
                  relief="flat", bd=0, cursor="hand2",
                  pady=5, activebackground=C["danger"],
                  command=self._remove_cart_item).pack(
            pady=(0, 6), padx=8, fill="x")

        # 3. Cart Table (Expands in the middle space between Header and Bottom Wrapper)
        cart_frame = tk.Frame(parent, bg=C["surface"],
                               highlightbackground=C["raspberry_dk"],
                               highlightthickness=1)
        cart_frame.pack(side="top", fill="both", expand=True, pady=(0, 6))

        cols  = ("icon", "name", "qty", "price", "total")
        heads = ("", "Product", "Qty", "Price", "Total")
        tf, self.cart_tree = u.scrollable_tree(
            cart_frame, cols, heads, height=12)
        tf.pack(fill="both", expand=True, padx=4, pady=4)

        self.cart_tree.column("icon",  width=36, anchor="center")
        self.cart_tree.column("name",  width=130)
        self.cart_tree.column("qty",   width=40, anchor="center")
        self.cart_tree.column("price", width=72, anchor="e")
        self.cart_tree.column("total", width=82, anchor="e")

        # ── Items packed inside the secure Bottom Wrapper ──

        # Totals block
        tot = tk.Frame(bottom_wrap, bg=C["surface"],
                        highlightbackground=C["blue"],
                        highlightthickness=1)
        tot.pack(fill="x", pady=(0, 6))
        tk.Frame(tot, bg=C["blue"], height=3).pack(fill="x")

        ti = tk.Frame(tot, bg=C["surface"])
        ti.pack(fill="x", padx=16, pady=10)

        self.subtotal_var = tk.StringVar(value="₹0.00")
        self.tax_var      = tk.StringVar(value="₹0.00")
        self.total_var    = tk.StringVar(value="₹0.00")

        for r, label, var, clr in [
            (0, "Subtotal",  self.subtotal_var, C["text"]),
            (1, "GST (5%)", self.tax_var,      C["text_dim"]),
        ]:
            tk.Label(ti, text=label, font=u.FONTS["label"],
                     bg=C["surface"], fg=C["text_dim"]).grid(
                row=r, column=0, sticky="w", pady=2)
            tk.Label(ti, textvariable=var, font=u.FONTS["mono"],
                     bg=C["surface"], fg=clr).grid(
                row=r, column=1, sticky="e", pady=2)

        tk.Frame(ti, bg=C["raspberry_dk"], height=1).grid(
            row=2, column=0, columnspan=2,
            sticky="ew", pady=5)

        tk.Label(ti, text="TOTAL",
                 font=("Georgia", 13, "bold"),
                 bg=C["surface"],
                 fg=C["raspberry2"]).grid(row=3, column=0, sticky="w")
        tk.Label(ti, textvariable=self.total_var,
                 font=("Georgia", 16, "bold"),
                 bg=C["surface"],
                 fg=C["raspberry2"]).grid(row=3, column=1, sticky="e")
        ti.columnconfigure(1, weight=1)

        # Payment block
        pay = tk.Frame(bottom_wrap, bg=C["surface"],
                        highlightbackground=C["border"],
                        highlightthickness=1)
        pay.pack(fill="x", pady=(0, 6))
        tk.Frame(pay, bg=C["blue"], height=3).pack(fill="x")

        pi = tk.Frame(pay, bg=C["surface"])
        pi.pack(fill="x", padx=14, pady=8)

        tk.Label(pi, text="PAYMENT METHOD",
                 font=u.FONTS["sub"],
                 bg=C["surface"], fg=C["blue3"]).pack(
            anchor="w", pady=(0, 6))

        self.payment_method = tk.StringVar(value="Cash")
        mf = tk.Frame(pi, bg=C["surface"])
        mf.pack(fill="x")
        for method, icon in [
            ("Cash", "💵"), ("UPI", "📱"), ("Card", "💳")
        ]:
            tk.Radiobutton(
                mf, text=f"{icon} {method}",
                variable=self.payment_method, value=method,
                bg=C["surface"], fg=C["text"],
                activebackground=C["surface"],
                selectcolor=C["raspberry_dk"],
                font=u.FONTS["label"],
                relief="flat",
            ).pack(side="left", padx=6)

        self.cash_frame = tk.Frame(pi, bg=C["surface"])
        self.cash_frame.pack(fill="x", pady=(6, 0))
        tk.Label(self.cash_frame, text="Cash Tendered ₹",
                 font=u.FONTS["label"],
                 bg=C["surface"], fg=C["text_dim"]).pack(side="left")
        self.cash_tendered = tk.StringVar()
        ttk.Entry(self.cash_frame,
                  textvariable=self.cash_tendered,
                  width=10).pack(side="left", padx=5, ipady=3)
        self.change_lbl = tk.Label(
            self.cash_frame, text="",
            font=u.FONTS["label"],
            bg=C["surface"], fg=C["success"])
        self.change_lbl.pack(side="left", padx=5)

        self.cash_tendered.trace_add("write", self._calc_change)
        self.payment_method.trace_add("write", self._toggle_cash)

        # Checkout Button (The bottom-most element)
        tk.Button(bottom_wrap,
                  text="✅  CHECKOUT & PRINT BILL",
                  font=("Helvetica", 11, "bold"),
                  bg=C["success"], fg="#000",
                  activebackground="#00C853",
                  relief="flat", bd=0,
                  cursor="hand2", pady=12,
                  command=self._checkout).pack(fill="x")

    # ── Product Grid Builder ──────────────────────────────────────────────────

    def _refresh_products(self):
        self.products = db.get_all_products()
        self._photo_refs.clear()

        for w in self.prod_grid.winfo_children():
            w.destroy()
        self._card_widgets.clear()

        COLS = 5 
        for i, p in enumerate(self.products):
            row = i // COLS
            col = i % COLS
            self._make_billing_card(self.prod_grid, p, row, col)

        for c in range(COLS):
            self.prod_grid.columnconfigure(c, weight=1)

    def _make_billing_card(self, parent, product, row, col):
        C    = u.COLORS
        icon = u.get_product_icon(product["name"])
        name = product["name"]
        img_path = _get_product_image_path(name)

        in_stock   = product["stock"] > 0
        card_bg    = C["surface"]  if in_stock else C["surface2"]
        icon_bg    = C["surface2"] if in_stock else C["bg"]
        name_color = C["text"]     if in_stock else C["text_muted"]
        border_col = C["border"]   if in_stock else C["text_muted"]

        card = tk.Frame(parent, bg=card_bg,
                        highlightbackground=border_col,
                        highlightthickness=1,
                        cursor="hand2" if in_stock else "")
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        tk.Frame(card, bg=C["raspberry"] if in_stock
                 else C["text_muted"], height=3).pack(fill="x")

        icon_f = tk.Frame(card, bg=icon_bg, width=140, height=95)
        icon_f.pack(fill="x", padx=8, pady=(8, 3))
        icon_f.pack_propagate(False)

        if img_path:
            photo = _load_tk_image(img_path, size=(138, 93))
            if photo:
                self._photo_refs.append(photo)
                tk.Label(icon_f, image=photo, bg=icon_bg).pack(expand=True)
            else:
                tk.Label(icon_f, text="🖼", font=("Helvetica", 36),
                         bg=icon_bg, fg=C["text_muted"]).pack(expand=True)
        else:
            tk.Label(icon_f, text=icon, font=("Helvetica", 38),
                     bg=icon_bg,
                     fg=C["raspberry2"] if in_stock else C["text_muted"]).pack(expand=True)

        tk.Label(card, text=name,
                 font=u.FONTS["label_b"],
                 bg=card_bg, fg=name_color,
                 wraplength=130,
                 justify="center").pack(padx=6, pady=(3, 1))

        tk.Label(card,
                 text=f"₹{float(product['price']):.2f}",
                 font=("Georgia", 12, "bold"),
                 bg=card_bg,
                 fg=C["raspberry2"] if in_stock else C["text_muted"]).pack()

        stock_val   = product["stock"]
        pill_color  = (C["danger"]  if stock_val == 0 else
                       C["warning"] if stock_val <= 5  else
                       C["success"])
        pill_bg     = C["bg"]
        pill_text   = ("OUT OF STOCK" if stock_val == 0
                       else f"Stock: {stock_val}")

        pill = tk.Frame(card, bg=pill_bg,
                        highlightbackground=pill_color,
                        highlightthickness=1)
        pill.pack(padx=8, pady=(3, 8), fill="x")
        tk.Label(pill, text=pill_text,
                 font=u.FONTS["small"],
                 bg=pill_bg, fg=pill_color).pack(pady=2)

        self._card_widgets[name] = card

        if in_stock:
            def on_click(event, p=product, c=card):
                self._select_billing_card(p, c)

            self._bind_children_click(card, on_click)

            def on_enter(e, c=card):
                c.config(highlightbackground=C["raspberry2"],
                         highlightthickness=2)
            def on_leave(e, c=card, bc=border_col):
                c.config(highlightbackground=bc,
                         highlightthickness=1)
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

    def _bind_children_click(self, widget, command):
        widget.bind("<Button-1>", command)
        for child in widget.winfo_children():
            self._bind_children_click(child, command)

    def _select_billing_card(self, product, card_widget):
        C = u.COLORS

        for name, c in self._card_widgets.items():
            try:
                c.config(highlightbackground=C["border"],
                         highlightthickness=1)
            except Exception:
                pass

        card_widget.config(highlightbackground=C["raspberry2"],
                            highlightthickness=2)

        self._selected_product = product
        
        img_path = _get_product_image_path(product["name"])
        if img_path:
            photo = _load_tk_image(img_path, size=(40, 40))
            if photo:
                self._photo_refs.append(photo)
                self.selected_icon_lbl.config(image=photo, text="")
            else:
                self.selected_icon_lbl.config(image="", text="🖼", font=("Helvetica", 20))
        else:
            icon = u.get_product_icon(product["name"])
            self.selected_icon_lbl.config(image="", text=icon, font=("Helvetica", 20))

        self.selected_name_lbl.config(text=product["name"])
        self.selected_price_lbl.config(
            text=f"₹{float(product['price']):.2f}")
        self.selected_stock_lbl.config(
            text=f"(Available: {product['stock']})")
        self.qty_var.set(1)

    # ── Cart Helpers ──────────────────────────────────────────────────────────

    def _add_to_cart(self):
        if not self._selected_product:
            messagebox.showwarning("No Selection",
                "Please click on a product card first.")
            return

        product = self._selected_product
        name    = product["name"]
        try:
            qty = self.qty_var.get()
        except tk.TclError:
            messagebox.showwarning("Invalid Quantity", "Please enter a valid number.")
            return

        if qty <= 0:
            messagebox.showwarning("Quantity",
                "Quantity must be at least 1.")
            return

        existing = next(
            (i for i in self.cart if i["name"] == name), None)
        cart_qty = existing["qty"] if existing else 0

        if cart_qty + qty > product["stock"]:
            messagebox.showerror("Stock Error",
                f"Only {product['stock']} in stock "
                f"({cart_qty} already in cart).")
            return

        if existing:
            existing["qty"] += qty
        else:
            self.cart.append({
                "name":  name,
                "price": float(product["price"]),
                "qty":   qty,
            })

        self._refresh_cart_display()
        u.show_toast(self, f"Added {qty}× {name}", kind="rasp")

    def _refresh_cart_display(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        subtotal = 0.0
        for i, item in enumerate(self.cart):
            line = item["price"] * item["qty"]
            subtotal += line
            tag  = "odd" if i % 2 else "even"
            icon = u.get_product_icon(item["name"])
            self.cart_tree.insert("", "end", values=(
                icon,
                item["name"],
                item["qty"],
                f"₹{item['price']:.2f}",
                f"₹{line:.2f}",
            ), tags=(tag,))

        tax   = subtotal * 0.05
        total = subtotal + tax
        self.subtotal_var.set(u.currency(subtotal))
        self.tax_var.set(u.currency(tax))
        self.total_var.set(u.currency(total))
        self._calc_change()

    def _remove_cart_item(self):
        sel = self.cart_tree.selection()
        if not sel:
            return
        vals = self.cart_tree.item(sel[0])["values"]
        name = vals[1]
        self.cart = [i for i in self.cart if i["name"] != name]
        self._refresh_cart_display()
        u.show_toast(self, f"Removed {name}", kind="warning")

    def _toggle_cash(self, *_):
        if self.payment_method.get() == "Cash":
            self.cash_frame.pack(fill="x", pady=(6, 0))
        else:
            self.cash_frame.pack_forget()

    def _calc_change(self, *_):
        try:
            tender_str = self.cash_tendered.get().strip()
            if not tender_str:
                self.change_lbl.config(text="")
                return
            
            tendered = float(tender_str)
            total_clean = self.total_var.get().replace("₹","").replace(",","").strip()
            total = float(total_clean)
            
            change = tendered - total
            if change >= 0:
                self.change_lbl.config(
                    text=f"Change: {u.currency(change)}",
                    fg=u.COLORS["success"])
            else:
                self.change_lbl.config(
                    text=f"Short: {u.currency(abs(change))}",
                    fg=u.COLORS["danger"])
        except ValueError:
            self.change_lbl.config(text="")

    # ── Checkout ──────────────────────────────────────────────────────────────

    def _checkout(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart",
                "Add items to cart before checkout.")
            return

        cust_name  = self.cust_name.get().strip()  or "Walk-in Customer"
        cust_phone = self.cust_phone.get().strip() or "—"
        payment    = self.payment_method.get()

        if payment == "Cash":
            tender_str = self.cash_tendered.get().strip()
            if not tender_str:
                messagebox.showwarning("Cash Required", "Please enter the cash tendered amount.")
                return
                
            try:
                tendered = float(tender_str)
                total_clean = self.total_var.get().replace("₹","").replace(",","").strip()
                total = float(total_clean)
                
                if tendered < total:
                    messagebox.showerror("Payment Error", "Cash tendered is less than the total bill amount.")
                    return
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid numerical cash amount.")
                return

        try:
            date_str = u.now_str()
            db.save_sale(self.bill_id, cust_name, cust_phone,
                         self.cart, payment, date_str)
            for item in self.cart:
                db.reduce_stock(item["name"], item["qty"])
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to complete checkout.\nError details: {e}")
            return

        # Snapshot the cart so the download button still works after we clear it!
        cart_snapshot = list(self.cart)
        self._show_receipt(cust_name, cust_phone, payment, date_str, cart_snapshot)

        # Reset
        self.cart = []
        self._selected_product = None
        self.bill_id = u.generate_bill_id()
        self._bill_lbl.config(text=f"Bill: {self.bill_id}")
        self.cust_name.set("")
        self.cust_phone.set("")
        self.cash_tendered.set("")
        self.selected_icon_lbl.config(image="", text="—")
        self.selected_name_lbl.config(text="No product selected")
        self.selected_price_lbl.config(text="")
        self.selected_stock_lbl.config(text="")
        self._refresh_cart_display()
        self._refresh_products()

    def _show_receipt(self, cust_name, cust_phone, payment, date_str, cart_items):
        C = u.COLORS
        win = tk.Toplevel(self)
        win.title("Receipt")
        win.geometry("480x680")
        win.configure(bg=C["bg"])
        win.resizable(False, False)
        u.apply_theme(win)

        tk.Frame(win, bg=C["raspberry"], height=5).pack(fill="x")

        frame = tk.Frame(win, bg=C["surface"],
                          highlightbackground=C["raspberry_dk"],
                          highlightthickness=1)
        frame.pack(fill="both", expand=True, padx=14, pady=14)

        inner = tk.Frame(frame, bg=C["surface"])
        inner.pack(fill="both", expand=True, padx=20, pady=20)

        def lbl(text, font=None, color=None, anchor="center"):
            tk.Label(inner, text=text,
                     font=font or u.FONTS["body"],
                     bg=C["surface"],
                     fg=color or C["text"],
                     justify="left" if anchor == "w" else "center",
                     anchor=anchor).pack(fill="x", pady=1)

        lbl("🛒  SuperMart", u.FONTS["heading"], C["raspberry2"])
        lbl("Official Receipt", u.FONTS["small"], C["text_dim"])
        lbl("─" * 50, color=C["border"])
        lbl(f"Bill ID  : {self.bill_id}", u.FONTS["small"], anchor="w")
        lbl(f"Date     : {date_str}",     u.FONTS["small"], anchor="w")
        lbl(f"Customer : {cust_name}",    u.FONTS["small"], anchor="w")
        lbl(f"Phone    : {cust_phone}",   u.FONTS["small"], anchor="w")
        lbl(f"Payment  : {payment}",      u.FONTS["small"], anchor="w")
        lbl("─" * 50, color=C["border"])

        for item in cart_items:
            icon = u.get_product_icon(item["name"])
            line = (f"{icon} {item['name'][:20]:<20}  "
                    f"{item['qty']:>3}x ₹{item['price']:>7.2f}"
                    f" = ₹{item['qty']*item['price']:>8.2f}")
            lbl(line, u.FONTS["small"], anchor="w")

        lbl("─" * 50, color=C["border"])
        subtotal = sum(i["price"] * i["qty"] for i in cart_items)
        tax      = subtotal * 0.05
        total    = subtotal + tax
        lbl(f"{'Subtotal':<32} {u.currency(subtotal):>10}",
            u.FONTS["small"], anchor="w")
        lbl(f"{'GST (5%)':<32} {u.currency(tax):>10}",
            u.FONTS["small"], C["text_dim"], anchor="w")
        lbl("─" * 50, color=C["raspberry_dk"])
        lbl(f"{'TOTAL':<32} {u.currency(total):>10}",
            u.FONTS["mono"], C["raspberry2"], anchor="w")
        lbl("─" * 50, color=C["border"])
        lbl("Thank you for shopping at SuperMart! 🙏",
            u.FONTS["small"], C["blue3"])

        # ── Added Download & Close Buttons ──
        btn_frame = tk.Frame(inner, bg=C["surface"])
        btn_frame.pack(fill="x", pady=(14, 0))

        tk.Button(btn_frame, text="📥 Download PDF",
                  font=u.FONTS["btn"], bg=C["blue"], fg="#fff",
                  relief="flat", bd=0, cursor="hand2", pady=8,
                  command=lambda: self._download_receipt_pdf(
                      self.bill_id, cust_name, cust_phone, payment, date_str, cart_items
                  )).pack(side="left", expand=True, fill="x", padx=(0, 4))

        tk.Button(btn_frame, text="Close",
                  font=u.FONTS["btn"], bg=C["raspberry_dk"], fg="#fff",
                  relief="flat", bd=0, cursor="hand2", pady=8,
                  command=win.destroy).pack(side="left", expand=True, fill="x", padx=(4, 0))

        u.show_toast(self, "Checkout complete! ✅", kind="success")

    # ── PDF Generator Helper ──────────────────────────────────────────────────

    def _download_receipt_pdf(self, b_id, c_name, c_phone, pay, d_str, cart_items):
        try:
            from fpdf import FPDF
        except ImportError:
            messagebox.showerror("Missing Library", "Please install FPDF to generate PDFs:\npip install fpdf")
            return

        filepath = filedialog.asksaveasfilename(
            title="Save Receipt",
            defaultextension=".pdf",
            filetypes=[("PDF Document", "*.pdf")],
            initialfile=f"Receipt_{b_id}"
        )
        if not filepath:
            return

        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Title
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "SuperMart - Official Receipt", ln=True, align="C")
            pdf.ln(5)

            # Details
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 6, f"Bill ID: {b_id}", ln=True)
            pdf.cell(0, 6, f"Date: {d_str}", ln=True)
            pdf.cell(0, 6, f"Customer: {c_name}", ln=True)
            pdf.cell(0, 6, f"Phone: {c_phone}", ln=True)
            pdf.cell(0, 6, f"Payment: {pay}", ln=True)
            pdf.ln(5)

            # Table Header
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(70, 8, "Item", border=1)
            pdf.cell(30, 8, "Qty", border=1, align="C")
            pdf.cell(40, 8, "Price", border=1, align="R")
            pdf.cell(40, 8, "Total", border=1, align="R", ln=True)

            # Items
            pdf.set_font("Arial", '', 11)
            subtotal = 0.0
            for item in cart_items:
                line_total = item['qty'] * item['price']
                subtotal += line_total
                pdf.cell(70, 8, str(item['name'])[:30], border=1)
                pdf.cell(30, 8, str(item['qty']), border=1, align="C")
                pdf.cell(40, 8, f"Rs. {item['price']:.2f}", border=1, align="R")
                pdf.cell(40, 8, f"Rs. {line_total:.2f}", border=1, align="R", ln=True)

            tax = subtotal * 0.05
            total = subtotal + tax

            # Totals
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(140, 8, "Subtotal", align="R")
            pdf.cell(40, 8, f"Rs. {subtotal:.2f}", align="R", ln=True)

            pdf.set_font("Arial", '', 11)
            pdf.cell(140, 8, "GST (5%)", align="R")
            pdf.cell(40, 8, f"Rs. {tax:.2f}", align="R", ln=True)

            pdf.set_font("Arial", 'B', 12)
            pdf.cell(140, 10, "TOTAL", align="R")
            pdf.cell(40, 10, f"Rs. {total:.2f}", align="R", ln=True)

            pdf.ln(10)
            pdf.set_font("Arial", 'I', 11)
            pdf.cell(0, 10, "Thank you for shopping at SuperMart!", ln=True, align="C")

            pdf.output(filepath)
            messagebox.showinfo("Success", f"Receipt downloaded successfully to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to generate PDF:\n{e}")

    # ── Navigation ────────────────────────────────────────────────────────────

    def _go_admin(self):
        self.destroy()
        from admin import AdminPanel
        AdminPanel(self.user).mainloop()

    def _logout(self):
        self.destroy()
        from login import LoginScreen
        LoginScreen().mainloop()