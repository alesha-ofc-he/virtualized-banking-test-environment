import psycopg2
from psycopg2 import Error
import datetime

def init_db():
    try:
        conn = psycopg2.connect(dbname="vm_test_db", user="postgres", password="1234", host="localhost", port="5432")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vm_reports (
                id SERIAL PRIMARY KEY,
                timestamp VARCHAR(50),
                vm_name VARCHAR(100),
                vm_status VARCHAR(100),
                network_status VARCHAR(100),
                connectivity_status VARCHAR(100)
            )
        ''')
        conn.commit()
        print("Database initialized successfully")
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def log_report(report_data):
    try:
        conn = psycopg2.connect(dbname="vm_test_db", user="postgres", password="SecurePass2025", host="localhost", port="5432")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vm_reports (timestamp, vm_name, vm_status, network_status, connectivity_status)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            report_data["timestamp"],
            report_data["vm_name"],
            report_data["vm_status"],
            report_data["network_status"],
            report_data["connectivity_status"]
        ))
        conn.commit()
        print("Report logged to PostgreSQL")
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()