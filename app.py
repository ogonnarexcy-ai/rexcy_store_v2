from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps
from pathlib import Path

app = Flask(__name__)

# -----------------------------
# BASIC SETTINGS
# -----------------------------

app.secret_key = "rexcy_store_secret_2026"

DB = Path(__file__).with_name("store.db")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# -----------------------------
# DATABASE
# -----------------------------

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            image TEXT NOT NULL,
            seller_url TEXT NOT NULL
        )
    """)

    # Add 50 products only if the database is empty
    count = conn.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    if count == 0:

        products = [

            (
                "Wireless Headphones",
                "₦25,000",
                "https://images.unsplash.com/photo-1505740420928-5e560c06d30e",
                "https://www.jumia.com.ng/"
            ),

            (
                "Smart Watch",
                "₦35,000",
                "https://images.unsplash.com/photo-1523275335684-37898b6baf30",
                "https://www.jumia.com.ng/"
            ),

            (
                "Bluetooth Speaker",
                "₦20,000",
                "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1",
                "https://www.jumia.com.ng/"
            ),

            (
                "Power Bank",
                "₦18,000",
                "https://images.unsplash.com/photo-1609592424147-8a0a2b0e9b1d",
                "https://www.jumia.com.ng/"
            ),

            (
                "USB-C Charger",
                "₦12,000",
                "https://images.unsplash.com/photo-1583863788434-e58a36330cf0",
                "https://www.jumia.com.ng/"
            ),

            (
                "Wireless Mouse",
                "₦10,000",
                "https://images.unsplash.com/photo-1527814050087-3793815479db",
                "https://www.jumia.com.ng/"
            ),

            (
                "Mechanical Keyboard",
                "₦35,000",
                "https://images.unsplash.com/photo-1587829741301-dc798b83add3",
                "https://www.jumia.com.ng/"
            ),

            (
                "Laptop Stand",
                "₦15,000",
                "https://images.unsplash.com/photo-1524758631624-e2822e304c36",
                "https://www.jumia.com.ng/"
            ),

            (
                "Phone Tripod",
                "₦14,000",
                "https://images.unsplash.com/photo-1606986628253-5b6c6e8e1a9b",
                "https://www.jumia.com.ng/"
            ),

            (
                "Ring Light",
                "₦22,000",
                "https://images.unsplash.com/photo-1611532736597-de2d4265fba3",
                "https://www.jumia.com.ng/"
            ),

            (
                "Smartphone Holder",
                "₦8,000",
                "https://images.unsplash.com/photo-1586953208448-b95a79798f07",
                "https://www.jumia.com.ng/"
            ),

            (
                "USB Flash Drive",
                "₦9,000",
                "https://images.unsplash.com/photo-1625842268584-8f3296236761",
                "https://www.jumia.com.ng/"
            ),

            (
                "Memory Card",
                "₦7,500",
                "https://images.unsplash.com/photo-1593640408182-31c70c8268f5",
                "https://www.jumia.com.ng/"
            ),

            (
                "Webcam",
                "₦28,000",
                "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04",
                "https://www.jumia.com.ng/"
            ),

            (
                "Gaming Headset",
                "₦32,000",
                "https://images.unsplash.com/photo-1599669454699-248893623440",
                "https://www.jumia.com.ng/"
            ),

            (
                "Gaming Mouse",
                "₦18,000",
                "https://images.unsplash.com/photo-1527814050087-3793815479db",
                "https://www.jumia.com.ng/"
            ),

            (
                "Gaming Keyboard",
                "₦40,000",
                "https://images.unsplash.com/photo-1541140532154-b024d705b90a",
                "https://www.jumia.com.ng/"
            ),

            (
                "Laptop Backpack",
                "₦25,000",
                "https://images.unsplash.com/photo-1553062407-98eeb64c6a62",
                "https://www.jumia.com.ng/"
            ),

            (
                "Bluetooth Earbuds",
                "₦22,000",
                "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1",
                "https://www.jumia.com.ng/"
            ),

            (
                "Phone Case",
                "₦6,000",
                "https://images.unsplash.com/photo-1601593346740-925612772716",
                "https://www.jumia.com.ng/"
            ),

            (
                "Screen Protector",
                "₦4,000",
                "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9",
                "https://www.jumia.com.ng/"
            ),

            (
                "Fast Charging Cable",
                "₦6,500",
                "https://images.unsplash.com/photo-1558618666-fcd25c85cd64",
                "https://www.jumia.com.ng/"
            ),

            (
                "LED Desk Lamp",
                "₦16,000",
                "https://images.unsplash.com/photo-1507473885765-e6ed057f782c",
                "https://www.jumia.com.ng/"
            ),

            (
                "Portable Fan",
                "₦13,000",
                "https://images.unsplash.com/photo-1564510182790-9a6d1f6b3d7a",
                "https://www.jumia.com.ng/"
            ),

            (
                "Electric Kettle",
                "₦20,000",
                "https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5",
                "https://www.jumia.com.ng/"
            ),

            (
                "Water Bottle",
                "₦8,000",
                "https://images.unsplash.com/photo-1602143407151-7111542de6e8",
                "https://www.jumia.com.ng/"
            ),

            (
                "Travel Backpack",
                "₦30,000",
                "https://images.unsplash.com/photo-1553062407-98eeb64c6a62",
                "https://www.jumia.com.ng/"
            ),

            (
                "Sports Shoes",
                "₦35,000",
                "https://images.unsplash.com/photo-1542291026-7eec264c27ff",
                "https://www.jumia.com.ng/"
            ),

            (
                "Casual Sneakers",
                "₦32,000",
                "https://images.unsplash.com/photo-1549298916-b41d501d3772",
                "https://www.jumia.com.ng/"
            ),

            (
                "Wrist Watch",
                "₦28,000",
                "https://images.unsplash.com/photo-1524805444758-089113d48a6d",
                "https://www.jumia.com.ng/"
            ),

            (
                "Sunglasses",
                "₦15,000",
                "https://images.unsplash.com/photo-1511499767150-a48a237f0083",
                "https://www.jumia.com.ng/"
            ),

            (
                "Wallet",
                "₦12,000",
                "https://images.unsplash.com/photo-1627123424574-724758594e93",
                "https://www.jumia.com.ng/"
            ),

            (
                "T-Shirt",
                "₦10,000",
                "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab",
                "https://www.jumia.com.ng/"
            ),

            (
                "Hoodie",
                "₦25,000",
                "https://images.unsplash.com/photo-1556821840-3a63f95609a7",
                "https://www.jumia.com.ng/"
            ),

            (
                "Jeans",
                "₦22,000",
                "https://images.unsplash.com/photo-1542272604-787c3835535d",
                "https://www.jumia.com.ng/"
            ),

            (
                "Cap",
                "₦7,000",
                "https://images.unsplash.com/photo-1521369909029-2afed882baee",
                "https://www.jumia.com.ng/"
            ),

            (
                "Handbag",
                "₦30,000",
                "https://images.unsplash.com/photo-1584917865442-de89df76afd3",
                "https://www.jumia.com.ng/"
            ),

            (
                "Perfume",
                "₦25,000",
                "https://images.unsplash.com/photo-1541643600914-78b084683601",
                "https://www.jumia.com.ng/"
            ),

            (
                "Hair Dryer",
                "₦18,000",
                "https://images.unsplash.com/photo-1522338242992-e1a54906a8da",
                "https://www.jumia.com.ng/"
            ),

            (
                "Electric Shaver",
                "₦20,000",
                "https://images.unsplash.com/photo-1621605815971-fbc98d665033",
                "https://www.jumia.com.ng/"
            ),

            (
                "Fitness Band",
                "₦15,000",
                "https://images.unsplash.com/photo-1557935728-e6d1eaabe558",
                "https://www.jumia.com.ng/"
            ),

            (
                "Yoga Mat",
                "₦14,000",
                "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f",
                "https://www.jumia.com.ng/"
            ),

            (
                "Exercise Resistance Bands",
                "₦10,000",
                "https://images.unsplash.com/photo-1598289431512-b97b0917affc",
                "https://www.jumia.com.ng/"
            ),

            (
                "Coffee Maker",
                "₦45,000",
                "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6",
                "https://www.jumia.com.ng/"
            ),

            (
                "Blender",
                "₦30,000",
                "https://images.unsplash.com/photo-1570222094114-d054a817e56b",
                "https://www.jumia.com.ng/"
            ),

            (
                "Rice Cooker",
                "₦35,000",
                "https://images.unsplash.com/photo-1585515320310-259814833e62",
                "https://www.jumia.com.ng/"
            ),

            (
                "Mini Vacuum Cleaner",
                "₦20,000",
                "https://images.unsplash.com/photo-1558317374-067fb5f30001",
                "https://www.jumia.com.ng/"
            ),

            (
                "Desk Organizer",
                "₦9,000",
                "https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85",
                "https://www.jumia.com.ng/"
            ),

            (
                "Notebook",
                "₦5,000",
                "https://images.unsplash.com/photo-1531346878377-a5be20888e57",
                "https://www.jumia.com.ng/"
            ),

            (
                "LED Strip Lights",
                "₦12,000",
                "https://images.unsplash.com/photo-1565814329452-e1efa11c5b89",
                "https://www.jumia.com.ng/"
            )
        ]

        conn.executemany(
            """
            INSERT INTO products
            (name, price, image, seller_url)
            VALUES (?, ?, ?, ?)
            """,
            products
        )

    conn.commit()
    conn.close()


# -----------------------------
# ADMIN SECURITY
# -----------------------------

def admin_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))

        return view(*args, **kwargs)

    return wrapped


# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/")
def home():

    conn = get_db()

    products = conn.execute(
        "SELECT * FROM products ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        products=products
    )


# -----------------------------
# ADMIN LOGIN
# -----------------------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin_logged_in"] = True

            return redirect(
                url_for("admin_dashboard")
            )

        flash(
            "Incorrect username or password.",
            "error"
        )

    return render_template("login.html")


# -----------------------------
# ADMIN LOGOUT
# -----------------------------

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------

@app.route("/admin")
@admin_required
def admin_dashboard():

    conn = get_db()

    products = conn.execute(
        "SELECT * FROM products ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "admin.html",
        products=products
    )


# -----------------------------
# ADD PRODUCT
# -----------------------------

@app.route("/admin/add", methods=["POST"])
@admin_required
def add_product():

    name = request.form.get("name", "").strip()
    price = request.form.get("price", "").strip()
    image = request.form.get("image", "").strip()
    seller_url = request.form.get("seller_url", "").strip()

    if not all([
        name,
        price,
        image,
        seller_url
    ]):

        flash(
            "Please fill in every field.",
            "error"
        )

        return redirect(
            url_for("admin_dashboard")
        )

    conn = get_db()

    conn.execute(
        """
        INSERT INTO products
        (name, price, image, seller_url)
        VALUES (?, ?, ?, ?)
        """,
        (
            name,
            price,
            image,
            seller_url
        )
    )

    conn.commit()
    conn.close()

    flash(
        "Product added successfully!",
        "success"
    )

    return redirect(
        url_for("admin_dashboard")
    )


# -----------------------------
# DELETE PRODUCT
# -----------------------------

@app.route(
    "/admin/delete/<int:product_id>",
    methods=["POST"]
)
@admin_required
def delete_product(product_id):

    conn = get_db()

    conn.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    conn.commit()
    conn.close()

    flash(
        "Product deleted successfully!",
        "success"
    )

    return redirect(
        url_for("admin_dashboard")
    )


# -----------------------------
# START REXCY STORE
# -----------------------------

# Create the database when the app starts
init_db()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )