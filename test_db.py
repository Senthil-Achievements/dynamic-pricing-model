import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'smart_price_db'
}

def test_connection():
    print("--- Database Connection Test ---")
    try:
        print(f"Connecting to {db_config['host']} as {db_config['user']}...")
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("Successfully connected to the database!")
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"You're connected to database: {record[0]}")
            
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            if tables:
                print("Tables found in database:")
                for table in tables:
                    print(f"- {table[0]}")
            else:
                print("No tables found. Did you import 'smart_price.sql'?")
            
            cursor.close()
            conn.close()
    except Error as e:
        print(f"\n!!!! CONNECTION FAILED !!!!")
        print(f"Error Code: {e.errno}")
        print(f"SQL State: {e.sqlstate}")
        print(f"Error Message: {e.msg}")
        
        if e.errno == 2003:
            print("\nPOSSIBLE CAUSES:")
            print("1. XAMPP/MySQL is not running. Please start MySQL in XAMPP Control Panel.")
        elif e.errno == 1049:
            print("\nPOSSIBLE CAUSES:")
            print("1. Database 'smart_price_db' does not exist. Please import 'smart_price.sql' in phpMyAdmin.")
        elif e.errno == 1045:
            print("\nPOSSIBLE CAUSES:")
            print("1. Username or Password incorrect. Default XAMPP is 'root' with NO password.")
        else:
            print("\nPlease check your XAMPP settings and ensure MySQL is active.")

if __name__ == "__main__":
    test_connection()
