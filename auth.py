import sqlite3
import hashlib
import uuid
from typing import Optional

class AuthDB:
    def __init__(self, db_path='auth.db'):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            session_token TEXT
        )''')
        self.conn.commit()

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def signup(self, username: str, email: str, password: str) -> bool:
        try:
            self.conn.execute('''INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)''',
                (username, email, self.hash_password(password)))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login(self, username_or_email: str, password: str) -> Optional[str]:
        cur = self.conn.execute('''SELECT id FROM users WHERE (username=? OR email=?) AND password_hash=?''',
            (username_or_email, username_or_email, self.hash_password(password)))
        row = cur.fetchone()
        if row:
            token = str(uuid.uuid4())
            self.conn.execute('UPDATE users SET session_token=? WHERE id=?', (token, row[0]))
            self.conn.commit()
            return token
        return None

    def get_user_by_token(self, token: str) -> Optional[dict]:
        cur = self.conn.execute('SELECT username, email FROM users WHERE session_token=?', (token,))
        row = cur.fetchone()
        if row:
            return {'username': row[0], 'email': row[1]}
        return None 