import sqlite3
import json
import time
from typing import Optional, List

class SessionHistoryDB:
    def __init__(self, db_path='session_history.db'):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            timestamp REAL,
            files TEXT,
            summary TEXT
        )''')
        self.conn.commit()

    def add_session(self, user: str, files: List[str], summary: str):
        self.conn.execute('''INSERT INTO sessions (user, timestamp, files, summary) VALUES (?, ?, ?, ?)''',
            (user, time.time(), json.dumps(files), summary))
        self.conn.commit()

    def get_sessions(self, user: Optional[str] = None):
        if user:
            cur = self.conn.execute('SELECT * FROM sessions WHERE user=? ORDER BY timestamp DESC', (user,))
        else:
            cur = self.conn.execute('SELECT * FROM sessions ORDER BY timestamp DESC')
        return cur.fetchall() 