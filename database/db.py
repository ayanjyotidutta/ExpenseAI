import sqlite3
from flask import g
from werkzeug.security import generate_password_hash

DATABASE = 'expense_tracker.db'


def get_db():
    """Returns a SQLite connection with row_factory and foreign keys enabled"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys = ON')
    return db


def init_db():
    """Creates all tables using CREATE TABLE IF NOT EXISTS"""
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    ''')
    db.commit()


def seed_db():
    """Inserts sample data for development"""
    db = get_db()

    # Check if users table already has data
    user_count = db.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
    if user_count > 0:
        return

    # Insert demo user
    hashed_password = generate_password_hash('demo123')
    db.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        ('Demo User', 'demo@ExpenseAI.com', hashed_password)
    )
    db.commit()

    # Fetch the inserted user's id
    demo_user = db.execute('SELECT id FROM users WHERE email = ?', ('demo@ExpenseAI.com',)).fetchone()
    user_id = demo_user['id']

    # Insert 8 sample expenses covering all categories
    sample_expenses = [
        (user_id, 45.50, 'Food', '2026-04-01', 'Grocery shopping'),
        (user_id, 15.00, 'Transport', '2026-04-02', 'Taxi fare'),
        (user_id, 120.00, 'Bills', '2026-04-03', 'Monthly electricity'),
        (user_id, 35.00, 'Health', '2026-04-04', 'Pharmacy'),
        (user_id, 60.00, 'Entertainment', '2026-04-05', 'Movie tickets'),
        (user_id, 85.00, 'Shopping', '2026-04-06', 'New clothes'),
        (user_id, 25.00, 'Food', '2026-04-08', 'Restaurant dinner'),
        (user_id, 10.00, 'Other', '2026-04-10', 'Miscellaneous'),
    ]

    for expense in sample_expenses:
        db.execute(
            'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
            expense
        )

    db.commit()


def create_user(name, email, password_hash):
    """Creates a new user"""
    db = get_db()
    db.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)', (name, email, password_hash))
    db.commit()


def get_user_by_email(email):
    """Gets a user by email"""
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    return user
