import os
from db import get_db_connection
import mysql.connector
from tabulate import tabulate
from pwinput import pwinput
db_connection = get_db_connection()

def view_users():
    try:
        cursor = db_connection.cursor()

        cursor.execute("SELECT UserID, Username, Role FROM Users")
        users = cursor.fetchall()
        print(tabulate(users, headers=['User ID', 'Username', 'Role'], tablefmt='double_grid'))
    except mysql.connector.Error as err:
        print("Error viewing users: {}".format(err))
    finally:
        cursor.close()

def add_user():
    try:
        cursor = db_connection.cursor()
        print("Create User Account")
        role = input("Enter new user role 'admin' or 'staff': ")
        print("Enter user details: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        if role != 'admin' and role != 'staff':
            print("Invalid role.")
            return
        # Insert data into the table
        cursor.execute("""
            INSERT INTO Users (Username, Password, Role) 
            VALUES (%s, %s, %s)
        """, (username, password, role))
        
        db_connection.commit()

        print("User added successfully.")
        view_users()
    except mysql.connector.Error as err:
        print("Error adding user: {}".format(err))
    finally:
        cursor.close()

def update_user():
    try:
        cursor = db_connection.cursor()
        view_users()
        user_id = input("Enter User ID to update: ")
        username = input("Enter new username: ")
        password = input("Enter new password: ")
        role = input("Enter new role 'admin' or 'staff': ")
        if role != 'admin' and role != 'staff':
            print("Invalid role.")
            return
        # Update user details
        cursor.execute("""
            UPDATE Users 
            SET Username = %s, Password = %s, Role = %s
            WHERE UserID = %s
        """, (username, password, role, user_id))
        
        db_connection.commit()

        print("User details updated successfully.")
        view_users()
    except mysql.connector.Error as err:
        print("Error updating user: {}".format(err))
    finally:
        cursor.close()

def delete_user():
    try:
        cursor = db_connection.cursor()
        view_users()
        user_id = input("Enter User ID to delete: ")

        cursor.execute("DELETE FROM Users WHERE UserID = %s", (user_id,))
        db_connection.commit()

        print("User deleted successfully.")
        view_users()
    except mysql.connector.Error as err:
        print("Error deleting user: {}".format(err))
    finally:
        cursor.close()

def user_login():
    try:
        cursor = db_connection.cursor()
        print("Login")
        username = input("Enter username: ")
        password = pwinput("Enter password: ")

        cursor.execute("SELECT Role FROM Users WHERE Username = %s AND Password = %s", (username, password))
        role = cursor.fetchone()
        if role is None:
            print("Invalid username or password.")
            choice = input("Do you want to try again? (y/n): ")
            if choice.lower() == 'y':
                user_login()
            else:
                return
        role = role[0]
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Login successful.\nUser: {} Role: {}".format(username,role))
        return role
    except mysql.connector.Error as err:
        print("Error logging in: {}".format(err))
    finally:
        cursor.close()
