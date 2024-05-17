from db import get_db_connection
import mysql.connector
from tabulate import tabulate


db_connection = get_db_connection()
def add_customer():
    try:
        cursor = db_connection.cursor()

        while True:
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            phone = input("Enter phone number: ")
            address = input("Enter address: ")

            # Insert data into the table, excluding CustomerID
            cursor.execute("""
                INSERT INTO Customers (FirstName, LastName, Email, Phone, Address) 
                VALUES (%s, %s, %s, %s, %s)
            """, (first_name, last_name, email, phone, address))
            
            db_connection.commit()

            print("Customer added successfully.")
            view_customers()
            choice = input("Do you want to add another customer? (yes/no): ")
            if choice.lower() != 'yes':
                break
    except mysql.connector.Error as err:
        print("Error inserting customer: {}".format(err))
    finally:
        cursor.close()

def update_customer():
    try:
        view_customers()
        cursor = db_connection.cursor()

        customer_id = input("Enter Customer ID to update: ")
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email: ")
        phone = input("Enter phone number: ")
        address = input("Enter address: ")

        # Update customer details
        cursor.execute("""
            UPDATE Customers 
            SET FirstName = %s, LastName = %s, Email = %s, Phone = %s, Address = %s 
            WHERE CustomerID = %s
        """, (first_name, last_name, email, phone, address, customer_id))
        
        db_connection.commit()

        print("Customer details updated successfully.")
        view_customers()
    except mysql.connector.Error as err:
        print("Error updating customer: {}".format(err))
    finally:
        cursor.close()

def delete_customer():
    try:
        view_customers()
        cursor = db_connection.cursor()

        customer_id = input("Enter Customer ID/email to delete: ")
        if '@' in customer_id:
            cursor.execute("SELECT CustomerID FROM Customers WHERE Email = %s", (customer_id,))
            customer_id = cursor.fetchone()
            if customer_id is None:
                print("Customer not found.")
                return
            customer_id = customer_id[0]
        # Delete customer details
        cursor.execute("""
            DELETE FROM Customers 
            WHERE CustomerID = %s
        """, (customer_id,))
        
        db_connection.commit()

        print("Customer deleted successfully.")
        view_customers()
    except mysql.connector.Error as err:
        print("Error deleting customer: {}".format(err))
    finally:
        cursor.close()

def view_customers():
    try:
        cursor = db_connection.cursor()
        print("Fetching customers...")
        print("Custmor details: ")
        cursor.execute("SELECT * FROM Customers")
        customers = cursor.fetchall()
        mydata = []
        for customer in customers:
            mydata.append([customer[0], customer[1], customer[2], customer[3], customer[4], customer[5]])
        print(tabulate(mydata, headers=["CustomerID", "FirstName", "LastName", "Email", "Phone", "Address"], tablefmt="double_grid"))
        db_connection.commit()
        # print("CustomerID\tFirstName\tLastName\tEmail\tPhone\tAddress")
        # for customer in customers:
        #     print("{}\t{}\t{}\t{}\t{}\t{}".format(customer[0], customer[1], customer[2], customer[3], customer[4], customer[5]))
    except mysql.connector.Error as err:
        print("Error fetching customers: {}".format(err))
    finally:
        cursor.close()