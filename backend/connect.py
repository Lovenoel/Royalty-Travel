import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='royalty_travel',
        password='royalty@travel01',
        database='royalty-travel'
    )
    print("Connection successful!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if conn:
        conn.close()
