import sqlite3
from typing import Optional

class FeedbackDB:
    def __init__(self, db_path='feedback.db'):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            line INTEGER,
            explanation TEXT,
            fix TEXT,
            rating INTEGER,
            comment TEXT
        )''')
        self.conn.commit()

    def add_feedback(self, filename: str, line: int, explanation: str, fix: str, rating: int, comment: Optional[str] = None):
        self.conn.execute('''INSERT INTO feedback (filename, line, explanation, fix, rating, comment)
            VALUES (?, ?, ?, ?, ?, ?)''', (filename, line, explanation, fix, rating, comment))
        self.conn.commit()

    def get_feedback(self, filename: Optional[str] = None):
        if filename:
            cur = self.conn.execute('SELECT * FROM feedback WHERE filename=?', (filename,))
        else:
            cur = self.conn.execute('SELECT * FROM feedback')
        return cur.fetchall() 