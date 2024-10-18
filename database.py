import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS scores (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                score REAL
                            )''')
        self.conn.commit()

    def save_score(self, name, score):
        self.cursor.execute('INSERT INTO scores (name, score) VALUES (?, ?)', (name, score))
        self.conn.commit()

    def get_top_scores(self, limit=5):
        self.cursor.execute('SELECT name, score FROM scores ORDER BY score DESC LIMIT ?', (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
