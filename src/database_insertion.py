import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from utils import get_db_connection, execute_sql_file
from data_transformation import run_data_transformation # Import the transformation function
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables

def insert_dataframe_into_mysql(df, table_name, db_connection):
    """Inserts a Pandas DataFrame into a specified MySQL table."""
    if df.empty:
        print(f"DataFrame for table '{table_name}' is empty. Skipping insertion.")
        return

    try:
        # Using SQLAlchemy engine for efficient bulk insertion
        # This requires 'pip install sqlalchemy PyMySQL'
        # Ensure you have 'PyMySQL' installed as mysql-connector-python with SQLAlchemy might be tricky
        # Or stick to mysql-connector-python's executemany for simpler approach
        db_connection_str = (
            f"mysql+mysqlconnector://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/"
            f"{os.getenv('DB_NAME')}"
        )
        engine = create_engine(db_connection_str)
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False, chunksize=1000)
        print(f"Successfully inserted {len(df)} rows into '{table_name}'.")

    except Exception as e:
        print(f"Error inserting into '{table_name}': {e}")
        # Fallback to executemany if sqlalchemy gives issues or for direct mysql.connector
        print("Attempting with mysql-connector-python's executemany as a fallback...")
        cursor = db_connection.cursor()
        cols = ", ".join([f"`{col}`" for col in df.columns]) # Enclose column names in backticks
        placeholders = ", ".join(["%s"] * len(df.columns))
        sql = f"INSERT INTO `{table_name}` ({cols}) VALUES ({placeholders})"
        try:
            data_to_insert = [tuple(row) for row in df.values]
            cursor.executemany(sql, data_to_insert)
            db_connection.commit()
            print(f"Successfully inserted {len(df)} rows into '{table_name}' using executemany.")
        except mysql.connector.Error as err:
            print(f"Error with executemany for '{table_name}': {err}")
            db_connection.rollback()
        finally:
            cursor.close()


def populate_all_tables():
    """Executes SQL file to create tables and then populates them with transformed data."""
    sql_file_path = "sql/create_tables.sql"
    execute_sql_file(sql_file_path) # Create tables first

    db_conn = get_db_connection()
    if not db_conn:
        print("Could not establish database connection. Exiting.")
        return

    try:
        print("Starting data transformation for database insertion...")
        transformed_dfs = run_data_transformation()
        print("Data transformation complete. Beginning database insertion...")

        insert_dataframe_into_mysql(transformed_dfs['agg_transactions'], 'aggregated_transactions', db_conn)
        insert_dataframe_into_mysql(transformed_dfs['agg_users'], 'aggregated_users', db_conn)
        insert_dataframe_into_mysql(transformed_dfs['map_transactions'], 'map_transactions', db_conn)
        insert_dataframe_into_mysql(transformed_dfs['map_users'], 'map_users', db_conn)
        insert_dataframe_into_mysql(transformed_dfs['top_transactions_pincode'], 'top_transactions_pincode', db_conn)
        insert_dataframe_into_mysql(transformed_dfs['top_users_pincode'], 'top_users_pincode', db_conn)
        insert_dataframe_into_mysql(transformed_dfs['top_transactions_district'], 'top_transactions_district', db_conn)
        insert_dataframe_into_mysql(transformed_dfs['top_users_district'], 'top_users_district', db_conn)

        print("All data inserted into MySQL database.")
    except Exception as e:
        print(f"An error occurred during database population: {e}")
    finally:
        db_conn.close()

if __name__ == "__main__":
    populate_all_tables()