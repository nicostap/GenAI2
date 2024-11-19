import os
import sqlite3

DB_FOLDER = "./database"
DB_FILE = f"{DB_FOLDER}/database.db"
os.makedirs(DB_FOLDER, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_FILE)


def run_migrations():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT NULL
        )
        """)


def query_dql(query):
    """Run a DQL query"""
    print("DQL " + query)
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            print(results)
            if len(results) == 0:
                return {"message": "No item found"}
            return results
    except sqlite3.Error as e:
        return {"message": f"Error: {str(e)}"}


def query_dml(query):
    """Run a DML query"""
    print("DML " + query)
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            print("Success")
            return {"message": "Success"}
    except sqlite3.Error as e:
        return {"message": f"Error: {str(e)}"}


def query_ddl(query):
    print("DDL " + query)
    """Run a DDL query"""
    return {"message": "Error: DDL Operation not allowed"}
