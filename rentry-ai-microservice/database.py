import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv
import json

load_dotenv()

def get_db_connection():
    """Creates database connection using same config as Node.js app"""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except Exception as e:
        print(f" Database connection failed: {e}")
        return None

def get_db_products():
    """Fetches products from PostgreSQL database. Falls back to CSV if DB is offline."""
    conn = get_db_connection()
    
    try:
        if conn:
            # 1. Try Live Database first
            cursor = conn.cursor()
            
            # Query products table - adjust column names based on your schema
            query = """
            SELECT id, name, description, price, category, images 
            FROM products 
            WHERE is_available = true
            ORDER BY created_at DESC
            """
            
            cursor.execute(query)
            products = cursor.fetchall()
            
            # Convert to list of dictionaries
            product_list = []
            for row in products:
                product_list.append({
                    'id': row[0],
                    'name': row[1], 
                    'description': row[2],
                    'price': float(row[3]),
                    'category': row[4],
                    'image_url': row[5]
                })
            
            cursor.close()
            conn.close()
            
            print(f" Successfully fetched {len(product_list)} products from database")
            return product_list
            
    except Exception as e:
        print(f"⚠️ Database error: {e}. Reading from CSV instead.")
        
        # 2. Use CSV as fallback
        try:
            df = pd.read_csv("pricing_data.csv")
            # Convert CSV rows into format the AI expects
            mock_list = []
            for _, row in df.iterrows():
                mock_list.append({
                    'id': row.get('id', ''),
                    'name': row.get('name', ''),
                    'description': row.get('description', ''),
                    'price': float(row.get('price', 0)),
                    'category': row.get('category', ''),
                    'image_url': row.get('image_url', '')
                })
            return mock_list
        except Exception as e:
            print(f" Could not even read CSV: {e}")
            return []
    finally:
        if conn:
            conn.close()

def get_product_by_id(product_id):
    """Get a single product by ID from database"""
    conn = get_db_connection()
    
    try:
        if conn:
            cursor = conn.cursor()
            
            query = """
            SELECT id, name, description, price, category, images, owner_id
            FROM products 
            WHERE id = %s AND is_available = true
            """
            
            cursor.execute(query, (product_id,))
            product = cursor.fetchone()
            
            if product:
                product_dict = {
                    'id': product[0],
                    'name': product[1], 
                    'description': product[2],
                    'price': float(product[3]),
                    'category': product[4],
                    'image_url': product[5],
                    'owner_id': product[6]
                }
                cursor.close()
                return product_dict
            else:
                return None
                
    except Exception as e:
        print(f" Error fetching product {product_id}: {e}")
        return None
    finally:
        if conn:
            conn.close()

def test_connection():
    """Test database connection"""
    conn = get_db_connection()
    if conn:
        print(" Database connection successful")
        conn.close()
        return True
    else:
        print(" Database connection failed")
        return False

if __name__ == "__main__":
    test_connection()