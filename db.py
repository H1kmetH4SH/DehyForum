import sqlite3

# Connect to the database
conn = sqlite3.connect('forum.db')

# Create the table for storing posts
conn.execute('''CREATE TABLE IF NOT EXISTS posts
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              content TEXT NOT NULL);''')

# Create the table for storing comments
conn.execute('''CREATE TABLE IF NOT EXISTS comments
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              post_id INTEGER NOT NULL,
              content TEXT NOT NULL,
              FOREIGN KEY (post_id) REFERENCES posts(id));''')

# Commit the changes and close the connection
conn.commit()
conn.close()
