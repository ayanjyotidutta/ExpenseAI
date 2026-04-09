import sqlite3
from flask import g

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
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    ''')
    db.commit()


def seed_db():
    """Inserts sample data for development"""
    pass


def create_user(email, password):
    """Creates a new user"""
    db = get_db()
    db.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
    db.commit()


def get_user_by_email(email):
    """Gets a user by email"""
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    return user
