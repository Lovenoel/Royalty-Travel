'''
File that creates a new database user other than the root user
and gives that new user all the privileges of that database
'''

import mysql.connector
from mysql.connector import Error
import getpass


def create_user(username, password, host='localhost', database='`royalty-travel`'):
    """Creates the new database user with all privileges"""
    try:
        # Ask for the root password
        root_password = getpass.getpass("Enter MYSQL root password: ")

        # Connect to MySQL as root
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # MySQL root user
            password=root_password  # Root password provided by the user
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Check if the user already exists
            check_user_query = f"SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '{username}');"
            cursor.execute(check_user_query)
            user_exists = cursor.fetchone()[0]

            if user_exists:
                # If the user exists, update their password
                update_password_query = f"ALTER USER '{username}'@'{host}' IDENTIFIED BY '{password}';"
                cursor.execute(update_password_query)
                print(f"User '{username}' already exists. Password updated successfully!")
            else:
                # Create a new user
                create_user_query = f"CREATE USER '{username}'@'{host}' IDENTIFIED BY '{password}';"
                cursor.execute(create_user_query)
                print(f"User '{username}' created successfully!")

            # Ensure that the database exists before granting privileges
            use_database_query = f"USE {database};"
            cursor.execute(use_database_query)

            # Grant all privileges to the user on the specified database
            grant_privileges_query = f"GRANT ALL PRIVILEGES ON {database}.* TO '{username}'@'{host}';"
            cursor.execute(grant_privileges_query)
            print(f"Granted all privileges to '{username}' on database '{database}'.")

            # Apply the changes
            cursor.execute("FLUSH PRIVILEGES;")
            print("Privileges flushed!")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == '__main__':
    # Ask for the new user's username and password
    new_username = input("Enter the new username: ")
    new_password = getpass.getpass("Enter the new user's password: ")

    # Create the user
    create_user(new_username, new_password)

