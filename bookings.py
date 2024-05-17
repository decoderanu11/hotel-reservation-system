from db import get_db_connection
import mysql.connector
from tabulate import tabulate
from room import view_rooms
from customers import view_customers
from bills import generate_bill

db_connection = get_db_connection()
def make_booking():
    try:
        
        view_customers()
        cursor = db_connection.cursor()
        is_id = True
        customer_id = input("Enter Customer ID / Email: ")
        if '@' in str(customer_id):
            is_id = False

        if not is_id:
            cursor.execute("SELECT CustomerID FROM Customers WHERE Email = %s", (customer_id,))
            is_customer_id = cursor.fetchone()
            if not is_customer_id:
                print("Customer not found.")
                print("Enter Customer Details:")
                first_name = input("Enter First Name: ")
                last_name = input("Enter Last Name: ")
                email = customer_id
                phone = input("Enter Phone Number: ")
                address = input("Enter Address: ")
                cursor.execute("""
                    INSERT INTO Customers (FirstName, LastName, Email, Phone, Address)
                    VALUES (%s, %s, %s, %s, %s)
                """, (first_name, last_name, email, phone, address))
                db_connection.commit()
                print("Customer added successfully.")
                cursor.execute("SELECT CustomerID FROM Customers WHERE Email = %s", (email,))
                customer_id = cursor.fetchone()
                customer_id = customer_id[0]
                print("Created Customer ID:", customer_id)
            # customer_id = customer_id[0]
        
            


        check_in_date = input("Enter Check-in Date (YYYY-MM-DD): ")
        check_out_date = input("Enter Check-out Date (YYYY-MM-DD): ")
        print("Checking room availability...")


        is_avail = check_room_availability(check_in_date, check_out_date)
        if not is_avail:
            return
        room_id = int(input("Enter Room ID: "))
        number_of_guests = int(input("Enter Number of Guests: "))
        checkin = input("Is the customer making Checkin immediately (y/n)? - " )
        if checkin == 'y':
            status = 'Checkin'
        else:
            status = 'Booked'
        cursor.execute("""
            INSERT INTO Bookings (CustomerID, RoomID, CheckInDate, CheckOutDate, NumberOfGuests, Status) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (customer_id, room_id, check_in_date, check_out_date, number_of_guests, status))
        
        db_connection.commit()

        print("Booking made successfully.")
        view_bookings()
    except Exception as err:
        print("Error making booking: {}".format(err))
    finally:
        cursor.close()

def update_booking():
    try:
        cursor = db_connection.cursor()
        print("Viewing Bookings:")
        view_bookings()
        # Get the booking ID to update
        booking_id = int(input("Enter Booking ID to update: "))
        # Gather updated booking information from the user
        customer_id = int(input("Enter Customer ID: "))
        room_id = int(input("Enter Room ID: "))
        check_in_date = input("Enter Check-in Date (YYYY-MM-DD): ")
        check_out_date = input("Enter Check-out Date (YYYY-MM-DD): ")
        number_of_guests = int(input("Enter Number of Guests: "))
        status = input("Enter Status Booked, Cancelled, checkin, checkout: ")

        # Update the booking in the Bookings table
        cursor.execute("""
            UPDATE Bookings 
            SET CustomerID = %s, RoomID = %s, CheckInDate = %s, CheckOutDate = %s, NumberOfGuests = %s, Status = %s
            WHERE BookingID = %s
        """, (customer_id, room_id, check_in_date, check_out_date, number_of_guests, status, booking_id))
        
        db_connection.commit()

        print("Booking updated successfully.")
        view_bookings()
    except Exception as err:
        print("Error updating booking: {}".format(err))
    finally:
        cursor.close()

def cancel_booking():
    try:
        cursor = db_connection.cursor()
        view_bookings()
        # Get the booking ID to cancel
        booking_id = int(input("Enter Booking ID to cancel: "))

        # Delete the booking from the Bookings table
        cursor.execute("""
            UPDATE Bookings 
            SET Status = 'Cancelled'
            WHERE BookingID = %s
        """, (booking_id,))
        
        db_connection.commit()

        print("Booking canceled successfully.")
        view_bookings()
    except Exception as err:
        print("Error canceling booking: {}".format(err))
    finally:
        cursor.close()

def delete_booking():
    try:
        cursor = db_connection.cursor()
        view_bookings()
        # Get the booking ID to delete
        booking_id = int(input("Enter Booking ID to delete: "))

        # Delete the booking from the Bookings table
        cursor.execute("DELETE FROM Bookings WHERE BookingID = %s", (booking_id,))
        db_connection.commit()

        print("Booking deleted successfully.")
        view_bookings()
    except Exception as err:
        print("Error deleting booking: {}".format(err))
    finally:
        cursor.close()

def view_bookings():
    try:
        cursor = db_connection.cursor()

        # Fetch all bookings from the Bookings table
        cursor.execute("SELECT * FROM Bookings")
        bookings = cursor.fetchall()
        if not bookings:
            print("No bookings found.")
            return
        # Display the bookings
        print(tabulate(bookings, headers=['BookingID', 'CustomerID', 'RoomID', 'CheckInDate', 'CheckOutDate', 'NumberOfGuests', 'Status'], tablefmt="double_grid"))
    except Exception as err:
        print("Error viewing bookings: {}".format(err))
    finally:
        cursor.close()

def check_room_availability(check_in_date = None, check_out_date = None):
    try:
        if not check_in_date:
            check_in_date = input("Enter Check-in Date (YYYY-MM-DD): ")
        if not check_out_date:
            check_out_date = input("Enter Check-out Date (YYYY-MM-DD): ")
        cursor = db_connection.cursor()

        # Query to check room availability for the given date range
        cursor.execute("""
            SELECT RoomID 
            FROM Bookings 
            WHERE NOT (CheckOutDate <= %s OR CheckInDate >= %s) AND Status != 'Cancelled' AND Status != 'Checkout'
        """, (check_in_date, check_out_date))
        
        booked_rooms = cursor.fetchall()
        booked_rooms = [room[0] for room in booked_rooms]
        # print("Booked rooms:", booked_rooms)

        if not booked_rooms:
            cursor.execute("SELECT * FROM Rooms WHERE Status!='Unavailable'")
            rooms = cursor.fetchall()
            print(tabulate(rooms, headers=['RoomID', 'RoomType', 'Price', 'Status'], tablefmt="double_grid"))
            return True
        # print("Booked rooms:", booked_rooms)
        cursor.execute('''SELECT * 
                       FROM Rooms
                       WHERE RoomID NOT IN ({}) AND Status!="Unavailable"'''.format(', '.join(map(str, booked_rooms))))
        available_rooms = cursor.fetchall()
        if not available_rooms:
            print("No rooms available for the given date range.")
            return False
        else:
            print(tabulate(available_rooms, headers=['RoomID', 'RoomType', 'Price', 'Status'], tablefmt="double_grid"))
            return True
    except Exception as err:
        print("Error checking room availability: {}".format(err))
    finally:
        cursor.close()
def check_out():
    try:
        cursor = db_connection.cursor()
        view_bookings()
        booking_id = int(input("Enter Booking ID to check-out: "))
        
        cursor.execute("""
            UPDATE Bookings 
            SET Status = 'Checkout'
            WHERE BookingID = %s
        """, (booking_id,))

        db_connection.commit()
        print("Checked-out successfully.")
        generate_bill(booking_id)

        view_bookings()
    except Exception as err:
        print("Error checking out: {}".format(err))
    finally:
        cursor.close()

def check_in():
    try:
        cursor = db_connection.cursor()
        view_bookings()
        booking_id = int(input("Enter Booking ID to check-in: "))
        
        cursor.execute("""
            UPDATE Bookings 
            SET Status = 'Checkin'
            WHERE BookingID = %s
        """, (booking_id,))

        db_connection.commit()
        print("Checked-in successfully.")
        view_bookings()
    except Exception as err:
        print("Error checking in: {}".format(err))
    finally:
        cursor.close()
        