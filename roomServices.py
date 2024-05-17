from db import get_db_connection
import mysql.connector
from tabulate import tabulate

db_connection = get_db_connection()

def view_services():
    try:
        cursor = db_connection.cursor()

        cursor.execute("SELECT * FROM Services")
        services = cursor.fetchall()
        print("Room services: ")
        print(tabulate(services, headers=["ServiceID", "Service Name", "Service Price"], tablefmt="double_grid"))
    except mysql.connector.Error as err:
        print("Error fetching room services: {}".format(err))
    finally:
        cursor.close()

def add_service():
    try:
        cursor = db_connection.cursor()
        service_name = input("Enter Service Name: ")
        service_price = float(input("Enter Service Price: "))

        # Insert data into the table
        cursor.execute("""
            INSERT INTO Services (ServiceName, Price) 
            VALUES (%s, %s)
        """, (service_name, service_price))
        
        db_connection.commit()

        print("Room service added successfully.")
        view_services()
    except mysql.connector.Error as err:
        print("Error adding room service: {}".format(err))
    finally:
        cursor.close()

def update_service():
    try:
        cursor = db_connection.cursor()
        view_services()
        service_id = input("Enter Room Service ID to update: ")
        service_name = input("Enter new Service Name: ")
        service_price = float(input("Enter new Service Price: "))

        # Update room service details
        cursor.execute("""
            UPDATE Services 
            SET ServiceName = %s, Price = %s
            WHERE ServiceID = %s
        """, (service_name, service_price, service_id))
        
        db_connection.commit()

        print("Room service updated successfully.")
        view_services()
    except mysql.connector.Error as err:
        print("Error updating room service: {}".format(err))
    finally:
        cursor.close()

def delete_service():
    try:
        cursor = db_connection.cursor()
        view_services()
        service_id = input("Enter Service ID to delete: ")

        cursor.execute("""
            DELETE FROM Services 
            WHERE ServiceID = %s
        """, (service_id,))
        
        db_connection.commit()

        print("Room service deleted successfully.")
        view_services()
    except mysql.connector.Error as err:
        print("Error deleting room service: {}".format(err))
    finally:
        cursor.close()
