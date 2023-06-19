import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_file):
        """ initialize connection to the SQLite database """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.create_table()
        except Error as e:
            print(e)

    def create_table(self):
        """ create a table for storing chat messages """
        try:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY,
                    message TEXT NOT NULL,
                    sentiment_score REAL NOT NULL,
                    user TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
        except Error as e:
            print(e)

    def insert_comment(self, message, sentiment_score, user, timestamp):
        """ insert a new comment into the chat_messages table """
        try:
            self.conn.execute("""
                INSERT INTO chat_messages (message, sentiment_score, user, timestamp) 
                VALUES (?, ?, ?, ?)
            """, (message, sentiment_score, user, timestamp))
            self.conn.commit()
        except Error as e:
            print(e)

    def get_comment(self, message):
        """ retrieve a comment from the chat_messages table """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM chat_messages WHERE message=?", (message,))
        return cur.fetchone()
