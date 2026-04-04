# 🛒 SuperMart — Supermarket Billing System

A full-featured **Point of Sale (POS)** desktop application built with **Python (Tkinter)** and **MySQL**, featuring a modern Raspberry & Blue themed UI, product image support, billing, receipts, and business reports.

---

## 📸 Screenshots

| Screen | Description |
|---|---|
| 🔐 Login Page | Fullscreen background image with frosted glass card |
| 📦 Admin Panel | Product grid cards with image upload |
| 🛒 Billing Screen | Product grid selection with cart and checkout |
| 📊 Reports | Revenue KPIs, monthly summary, stock alerts |

---

## 🚀 Features

### 🔐 Login System
- Fullscreen login with **supermarket background image**
- Role-based access — **Admin** and **User**
- Show/hide password toggle
- Role selector (👤 User / 🔑 Admin) with access validation

### 📦 Admin Panel
- **Product Grid View** — 4-column card layout with icons/images
- Add, Edit, Delete products
- **Upload real product images** (PNG, JPG, JPEG, BMP, GIF)
- Auto emoji icons based on product name (fallback if no image)
- Stock badges — 🟢 Good / 🟡 Low / 🔴 Critical
- User management — Create and Delete users
- Export reports to **Excel (.xlsx)**, **CSV**, or **TXT**

### 🛒 Billing Screen
- **Product grid card selection** — click to select
- Out-of-stock products automatically greyed out
- Add to cart with quantity control
- Customer name and phone number capture
- Payment methods — 💵 Cash / 📱 UPI / 💳 Card
- Cash change calculator
- **GST (5%)** automatically calculated

### 🧾 Receipt
- Printable receipt popup with full bill details
- Shows product emoji icons, quantities, prices
- Bill ID, date, customer info, payment method
- Subtotal + GST + Total breakdown

### 📊 Reports
- **KPI Cards** — Total Revenue, Today's Revenue, Total Bills
- Monthly revenue summary table
- Low stock alert table (products with stock ≤ 10)
- One-click export to Excel / CSV / TXT

---

## 🗂️ Project Structure

```
SuperMarketApp/
│
├── main.py              # Entry point — initialises DB and launches login
├── database.py          # All MySQL database queries and table setup
├── login.py             # Login screen with background image
├── admin.py             # Admin panel (products, users, reports)
├── billing.py           # Billing screen with cart and checkout
├── utils.py             # Theme, colors, fonts, helper functions
├── bg_login.jpg         # Login page background image
│
├── product_images/      # Auto-created folder for uploaded product images
│   ├── Rice_1kg.jpg
│   ├── Milk_500ml.png
│   └── ...
│
└── README.md            # This file
```

---

## 🛠️ Requirements

### Software
| Requirement | Version |
|---|---|
| Python | 3.8 or higher |
| MySQL Server | 8.0 or higher |
| MySQL Workbench | Any recent version |

### Python Libraries
| Library | Purpose | Install Command |
|---|---|---|
| `tkinter` | GUI framework | ✅ Built into Python — no install needed |
| `mysql-connector-python` | MySQL database connection | `pip install mysql-connector-python` |
| `Pillow` | Product images & background photo | `pip install Pillow` |
| `openpyxl` | Export reports to Excel | `pip install openpyxl` |

---

## ⚙️ Installation & Setup

### Step 1 — Install Python
1. Go to **https://www.python.org/downloads/**
2. Download and run the installer
3. ⚠️ **Tick "Add Python to PATH"** before clicking Install Now

### Step 2 — Install Required Libraries
Open **Command Prompt** and run these one by one:

```bash
py -m pip install mysql-connector-python
py -m pip install Pillow
py -m pip install openpyxl
```

### Step 3 — Install MySQL
1. Go to **https://dev.mysql.com/downloads/installer/**
2. Download and install **MySQL Developer Default**
3. During setup, set a **root password** — write it down!

### Step 4 — Create the Database
1. Open **MySQL Workbench**
2. Connect to **Local instance MySQL**
3. In the query area, type and run (**Ctrl + Enter**):

```sql
CREATE DATABASE supermarket_db;
```

### Step 5 — Configure Database Password
1. Open `database.py` in Notepad
2. Find this section near the top:

```python
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "root",                 ← Already configured
    "database": "supermarket_db",
    "consume_results": True,
}
```

3. The password is already set to **`root`** — no changes needed
4. If your MySQL password is different from `root`, replace it with your actual password and save the file

### Step 6 — Run the Application
1. Open the `SuperMarketApp` folder in File Explorer
2. Click the address bar → type `cmd` → press **Enter**
3. Type:

```bash
python main.py
```

---

## 🔑 Default Login Credentials

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |

> ⚠️ Change the default password after first login by creating a new admin account.

---

## 🖥️ How to Use

### As Admin

#### Managing Products
1. Login as **Admin**
2. Go to the **📦 Products** tab
3. To **add a product**:
   - Click **🖼 Upload Image** to add a photo (optional)
   - Fill in Name, Price, Stock
   - Click **➕ Add Product**
4. To **edit a product**:
   - Click any product card to select it
   - Edit the fields on the left
   - Click **✏️ Update Selected**
5. To **delete a product**:
   - Click a product card to select it
   - Click **🗑 Delete Selected**

#### Managing Users
1. Go to the **👤 Users** tab
2. Fill in Username, Password, Role
3. Click **➕ Create User**
4. To delete a user — select from table → **🗑 Delete Selected**

#### Viewing Reports
1. Go to the **📊 Reports** tab
2. Click **🔄 Refresh Reports** to update
3. Click **📥 Export Data** to save as Excel / CSV / TXT

### As Cashier (User)

#### Creating a Bill
1. Login as **User**
2. Enter customer **Name** and **Phone** (optional)
3. Click any **product card** to select it
4. Set the **quantity** and click **➕ Add to Cart**
5. Repeat for more products
6. Select **payment method** (Cash / UPI / Card)
7. For Cash — enter amount tendered (change is auto-calculated)
8. Click **✅ CHECKOUT & PRINT BILL**
9. A receipt popup will appear with the full bill

---

## 🗄️ Database Tables

### `users`
| Column | Type | Description |
|---|---|---|
| id | INT | Auto-increment primary key |
| username | VARCHAR(100) | Unique login username |
| password | VARCHAR(255) | Login password |
| role | ENUM | `admin` or `user` |

### `products`
| Column | Type | Description |
|---|---|---|
| id | INT | Auto-increment primary key |
| name | VARCHAR(200) | Unique product name |
| price | DECIMAL(10,2) | Selling price in ₹ |
| stock | INT | Available quantity |

### `sales`
| Column | Type | Description |
|---|---|---|
| id | INT | Auto-increment primary key |
| bill_id | VARCHAR(50) | Unique bill identifier |
| customer_name | VARCHAR(200) | Customer name |
| customer_phone | VARCHAR(20) | Customer phone |
| product_name | VARCHAR(200) | Product sold |
| quantity | INT | Quantity sold |
| unit_price | DECIMAL(10,2) | Price per unit |
| total | DECIMAL(10,2) | Line total |
| payment_method | VARCHAR(50) | Cash / UPI / Card |
| date | DATETIME | Date and time of sale |

---

## 🎨 Theme & Design

| Element | Color |
|---|---|
| Background | Deep Navy `#0D0A1A` |
| Primary Accent | Raspberry `#C2185B` |
| Secondary Accent | Blue `#1565C0` |
| Light Blue | `#42A5F5` |
| Success | Green `#00E676` |
| Warning | Amber `#FFD740` |
| Danger | Red `#FF1744` |

---

## 🔧 Troubleshooting

| ❌ Problem | ✅ Fix |
|---|---|
| `python is not recognized` | Reinstall Python and tick **"Add Python to PATH"** |
| `No module named mysql.connector` | Run `py -m pip install mysql-connector-python` |
| `Cannot connect to MySQL` | Open MySQL Workbench — check MySQL Server is running |
| `Access denied for user root` | Wrong password in `database.py` — fix the `password` field |
| `Unknown database supermarket_db` | Run `CREATE DATABASE supermarket_db;` in MySQL Workbench |
| Background image not showing | Run `py -m pip install Pillow` |
| Excel export not working | Run `py -m pip install openpyxl` |
| Product images not showing | Run `py -m pip install Pillow` |

---

## 📦 Sample Products (Pre-loaded)

The app automatically loads these products on first run:

| Product | Price | Stock |
|---|---|---|
| Rice (1kg) | ₹55.00 | 100 |
| Wheat Flour (1kg) | ₹45.00 | 80 |
| Sugar (1kg) | ₹42.00 | 120 |
| Salt (1kg) | ₹18.00 | 200 |
| Cooking Oil (1L) | ₹130.00 | 60 |
| Milk (500ml) | ₹28.00 | 90 |
| Bread | ₹35.00 | 50 |
| Eggs (12pcs) | ₹72.00 | 40 |
| Butter (100g) | ₹55.00 | 35 |
| Tea Powder (250g) | ₹85.00 | 45 |

---

## 📋 Complete File Checklist

Before running, make sure your folder has all these files:

```
✅ main.py
✅ database.py
✅ login.py
✅ admin.py
✅ billing.py
✅ utils.py
✅ bg_login.jpg
```

---

## 👨‍💻 Built With

- **Python 3** — Core programming language
- **Tkinter** — GUI framework (built into Python)
- **MySQL** — Database backend
- **mysql-connector-python** — Python-MySQL bridge
- **Pillow (PIL)** — Image processing for product photos
- **openpyxl** — Excel export support

---

## 📄 License

This project is built for educational and personal business use.

---

*SuperMart POS System — Built with ❤️ using Python & Tkinter*
