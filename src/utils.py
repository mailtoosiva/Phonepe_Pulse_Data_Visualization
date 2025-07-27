import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

def get_db_connection():
    """Establates and returns a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if conn.is_connected():
            print("Successfully connected to MySQL database")
            return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def close_db_connection(conn, cursor):
    """Closes the database cursor and connection."""
    if cursor:
        cursor.close()
    if conn and conn.is_connected():
        conn.close()
        print("MySQL connection closed.")

def execute_sql_file(sql_file_path):
    """Executes SQL commands from a given file."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            with open(sql_file_path, 'r') as f:
                sql_script = f.read()
            # Split by semicolon to execute multiple statements
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            conn.commit()
            print(f"Successfully executed SQL from {sql_file_path}")
        except mysql.connector.Error as err:
            print(f"Error executing SQL from {sql_file_path}: {err}")
            conn.rollback() # Rollback in case of error
        finally:
            close_db_connection(conn, cursor)

# Add other helper functions here, e.g., for specific data cleaning steps
# or common data fetching patterns.