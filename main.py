"""
SuperMart — Supermarket Billing System
Entry point: initialises the database and launches the login screen.
"""

import database as db
from login import LoginScreen


def main():
    db.initialize_db()
    app = LoginScreen()
    app.mainloop()


if __name__ == "__main__":
    main()
