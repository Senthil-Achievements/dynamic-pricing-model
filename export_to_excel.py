import mysql.connector
import pandas as pd
import os

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'smart_price_db'
}

def export_inventory():
    try:
        # Establish database connection
        print("Connecting to database...")
        conn = mysql.connector.connect(**db_config)
        
        # SQL Query to fetch only Barcode and Product Name
        query = "SELECT barcode, product_name FROM products"
        
        # Read data into a pandas DataFrame
        print("Fetching inventory data...")
        df = pd.read_sql(query, conn)
        
        # Define output filename
        filename = "Inventory_List.xlsx"
        
        # Export to Excel
        print(f"Exporting to {filename}...")
        df.to_excel(filename, index=False, engine='openpyxl')
        
        print(f"SUCCESS: Inventory exported to {os.path.abspath(filename)}")
        
        conn.close()
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    export_inventory()
