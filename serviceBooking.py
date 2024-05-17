from db import get_db_connection
import mysql.connector
from tabulate import tabulate
from bookings import view_bookings
from roomServices import view_services

db_connection = get_db_connection()
def view_service_bookings():
    try:
        cursor = db_connection.cursor()

        cursor.execute("SELECT * FROM servicebookings")
        bookings = cursor.fetchall()
        print("Services Bookings: ")
        if not bookings:
            print("No bookings found.")
            return
        print(tabulate(bookings, headers=["ServiceBookingID", "BookingID", "ServiceID", "Quantity", "TotalPrice"], tablefmt="double_grid"))
    except mysql.connector.Error as err:
        print("Error fetching bookings: {}".format(err))
    finally:
        cursor.close()

def make_service_booking():
    try:
        cursor = db_connection.cursor()
        view_bookings()
        booking_id = int(input("Enter Booking ID: "))
        view_services()
        service_id = int(input("Enter Service ID: "))
        quantity = int(input("Enter Quantity: "))
        
        cursor.execute("SELECT Price FROM Services WHERE ServiceID = %s", (service_id,))
        service_price = cursor.fetchone()
        if service_price is None:
            print("Service not found.")
            return
        service_price = service_price[0]
        total_price = service_price * quantity

        # Insert data into the table
        cursor.execute("""
            INSERT INTO servicebookings (BookingID, ServiceID, Quantity, TotalPrice) 
            VALUES (%s, %s, %s, %s)
        """, (booking_id, service_id, quantity, total_price))
        
        db_connection.commit()

        print("Service booking added successfully.")
        view_service_bookings()
    except mysql.connector.Error as err:
        print("Error adding service booking: {}".format(err))
    finally:
        cursor.close()

def update_service_booking():
    try:
        cursor = db_connection.cursor()
        view_service_bookings()
        service_booking_id = int(input("Enter Service Booking ID to update: "))
        view_services()
        service_id = int(input("Enter new Service ID: "))
        view_bookings()
        booking_id = int(input("Enter new Booking ID: "))
        quantity = int(input("Enter new Quantity: "))
        
        cursor.execute("SELECT Price FROM Services WHERE ServiceID = %s", (service_id,))
        service_price = cursor.fetchone()
        if service_price is None:
            print("Service not found.")
            return
        service_price = service_price[0]
        total_price = service_price * quantity

        # Update service booking details
        cursor.execute("""
            UPDATE servicebookings 
            SET BookingID = %s, ServiceID = %s,
            Quantity = %s, TotalPrice = %s
            WHERE ServiceBookingID = %s
        """, (booking_id, service_id, quantity, total_price, service_booking_id))
        
        db_connection.commit()

        print("Service booking updated successfully.")
        view_service_bookings()
    except mysql.connector.Error as err:
        print("Error updating service booking: {}".format(err))
    finally:
        cursor.close()

def delete_service_booking():
    try:
        cursor = db_connection.cursor()
        view_service_bookings()
        service_booking_id = int(input("Enter Service Booking ID to delete: "))

        cursor.execute("""
            DELETE FROM servicebookings 
            WHERE ServiceBookingID = %s
        """, (service_booking_id,))
        
        db_connection.commit()

        print("Service booking deleted successfully.")
        view_service_bookings()
    except mysql.connector.Error as err:
        print("Error deleting service booking: {}".format(err))
    finally:
        cursor.close()
