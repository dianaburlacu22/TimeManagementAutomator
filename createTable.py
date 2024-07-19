import sqlite3

def create_database():
    with sqlite3.connect('hours.db') as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS hours (
                DATE TEXT NOT NULL,
                CATEGORY TEXT NOT NULL,
                HOURS REAL NOT NULL
            );
        ''')
        print("Database and table created successfully")

if __name__ == "__main__":
    create_database()
