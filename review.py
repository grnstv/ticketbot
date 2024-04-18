import sqlite3
# 0. Import types for annotation
# from sqlite3 import Connection

# 1. It's good practice to mark function input and output types
# def connect_to_db(db_name: str) -> Connection:
# 2. If exception occurred inside connect_to_db() it:
# a) has no return
# b) not raising any exception just a print msg, so the code placed bellow will execute causing more exceptions
# Set conn before try to None and return it only after try-except
def connect_to_db(db_name):
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except Exception as e:
        print(f"An error occurred: {e}")

# Every function that use Connection type as input have to trust us that conn!=None
# You can place something like if not conn: return
def create_table(conn):
    cursor = conn.cursor()
    # All python multiline spaces are preserving in string
    # With such formatting you will get sql like: users(            id ...            name ...)

    # Also check spelling:
    # CREATE TEBLE > CREATE TABLE,
    # PRIMARY KAY > PRIMARY KEY
    # You do not need AUTOINCREMENT keyword, as you marked col with PRIMARY KEY - it will increment automatically
    cursor.execute("""CREATE TEBLE users(
            id INTEGER PRIMARY KAY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER)""")
    # You do not need to commit() after CREATE TABLE
    # SQL causes automatic implicit commit after DDL transactions
    conn.commit()

# create annotation for args:
# (user_name: str, user_age: int)
def insert_user(conn, user_name, user_age):
    cursor = conn.cursor()
    # INSERT, not INSER
    # Make sure user_name is str, or better cast it to str(user_name)
    # And int(user_age) as well
    cursor.execute("INSER INTO users(name, age) VALUES(?, ?)", (user_name, user_age))
    conn.commit()

# Usage example
db_connection = connect_to_db('my_database.db')
create_table(db_connection)
insert_user(db_connection, 'Alice', 30)
# We left connection open after operations
# Moreover, everything of above can fail - and leave connection open
# Wrap it with try-finally
# try:
#   db_connection = connect_to_db
#   create_table
#   insert_user
# finally:
#   db_connection.close()

