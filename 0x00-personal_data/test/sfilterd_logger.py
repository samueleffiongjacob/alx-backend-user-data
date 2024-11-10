import mysql.connector
from mysql.connector import connection
from os import environ

def get_db():
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME", "holberton")
    connector = connection.MySQLConnection(
        host=db_host,
        port=environ.get("PERSONAL_DATA_DB_PORT", 3306),
        user=username,
        password=password,
        database=db_name)
    return connector

def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        );
    """)
    db.commit()

def insert_data():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO users (name, email) VALUES
        ('John Doe', 'john@example.com'),
        ('Jane Smith', 'jane@example.com');
    """)
    db.commit()

if __name__ == "__main__":
    create_table()
    insert_data()
