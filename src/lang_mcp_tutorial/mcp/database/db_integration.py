# db_integration.py
import os
import psycopg2
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
NEON_DB_URL = os.getenv('NEON_DB_URL')

def connect_to_db():
    """Establish a connection to the Neon database."""
    if not NEON_DB_URL:
        print("Error: NEON_DB_URL environment variable not set")
        return None
    try:
        conn = psycopg2.connect(NEON_DB_URL)
        print("Successfully connected to Neon database")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        traceback.print_exc()
        return None

def create_record(table: str, data: dict) -> dict:
    """Insert a new record into the specified table."""
    conn = connect_to_db()
    if not conn:
        return {"error": "Database connection failed"}
    
    try:
        with conn.cursor() as cur:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"
            cur.execute(query, list(data.values()))
            result = cur.fetchone()
            conn.commit()
            column_names = [desc[0] for desc in cur.description]
            return dict(zip(column_names, result))
    except Exception as e:
        print(f"Error creating record: {str(e)}")
        traceback.print_exc()
        return {"error": str(e)}
    finally:
        conn.close()

def read_records(table: str, condition: str = None, params: tuple = ()) -> list:
    """Read records from the specified table."""
    conn = connect_to_db()
    if not conn:
        return [{"error": "Database connection failed"}]
    
    try:
        with conn.cursor() as cur:
            query = f"SELECT * FROM {table}"
            if condition:
                query += f" WHERE {condition}"
            cur.execute(query, params)
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            return [dict(zip(column_names, row)) for row in results]
    except Exception as e:
        print(f"Error reading records: {str(e)}")
        traceback.print_exc()
        return [{"error": str(e)}]
    finally:
        conn.close()

def update_record(table: str, data: dict, condition: str, params: tuple) -> dict:
    """Update a record in the specified table."""
    conn = connect_to_db()
    if not conn:
        return {"error": "Database connection failed"}
    
    try:
        with conn.cursor() as cur:
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {condition} RETURNING *"
            cur.execute(query, list(data.values()) + list(params))
            result = cur.fetchone()
            conn.commit()
            if result:
                column_names = [desc[0] for desc in cur.description]
                return dict(zip(column_names, result))
            return {"message": "No record updated"}
    except Exception as e:
        print(f"Error updating record: {str(e)}")
        traceback.print_exc()
        return {"error": str(e)}
    finally:
        conn.close()

def delete_record(table: str, condition: str, params: tuple) -> dict:
    """Delete a record from the specified table."""
    conn = connect_to_db()
    if not conn:
        return {"error": "Database connection failed"}
    
    try:
        with conn.cursor() as cur:
            query = f"DELETE FROM {table} WHERE {condition} RETURNING *"
            cur.execute(query, params)
            result = cur.fetchone()
            conn.commit()
            if result:
                column_names = [desc[0] for desc in cur.description]
                return dict(zip(column_names, result))
            return {"message": "No record deleted"}
    except Exception as e:
        print(f"Error deleting record: {str(e)}")
        traceback.print_exc()
        return {"error": str(e)}
    finally:
        conn.close()

# Example usage for debugging
# data = create_record("users", {"name": "Jane Doe", "email": "jane@example.com"})
# print(data)
# records = read_records("users", "name = %s", ("Jane Doe",))
# print(records)