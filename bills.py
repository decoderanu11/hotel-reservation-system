from db import get_db_connection
import mysql.connector
from tabulate import tabulate
from util import print_horizontal_line
db_connection = get_db_connection()


def generate_bill(booking_id,PaymentStatus="Paid"):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM bookings WHERE BookingID = %s", (booking_id,))
        booking = cursor.fetchone()
        if booking is None:
            print("Booking not found.")
            return
        print("Room Details: ")
        print(tabulate([booking], headers=["BookingID", "CustomerID", "RoomID", "CheckInDate", "CheckOutDate", "NumberOfGuests"], tablefmt="double_grid"))
        cursor.execute("SELECT Price FROM rooms WHERE RoomID = %s", (booking[2],))
        room_price = cursor.fetchone()
        if room_price is None:
            print("Room not found.")
            return
        room_price = room_price[0]
        total_nights = (booking[4] - booking[3]).days


        cursor.execute("SELECT * FROM servicebookings WHERE BookingID = %s", (booking_id,))
        service_bookings = cursor.fetchall()
        total_service_price = 0
        if not service_bookings:
            print("No service bookings found.")
        else:
            print("\n Service bookings: ")
            print(tabulate(service_bookings, headers=["ServiceBookingID", "BookingID", "ServiceID", "Quantity", "TotalPrice"], tablefmt="double_grid"))
            for service_booking in service_bookings:
                total_service_price += service_booking[4]
        print("Room price per night: ", room_price)
        print("Total Nights: ", total_nights)
        total_room_price = float(room_price) * float(total_nights)
        print("Total Room Price: ", total_room_price)
        print("Total Service Price: ", total_service_price)
        total_price = float(total_room_price) + float(total_service_price)
        print("Total Amount: ", total_price)
        cursor.execute("""
            INSERT INTO bills (BookingID, RoomCost, ServiceCost, TotalAmount, PaymentStatus) 
            VALUES (%s, %s, %s, %s, %s)
        """, (booking_id, total_room_price, total_service_price, total_price, PaymentStatus))

        db_connection.commit()
    except mysql.connector.Error as err:
        print("Error making booking: {}".format(err))
    finally:
        cursor.close()


def view_bills(bill_id=None):
    try:
        print_horizontal_line()
        
        cursor = db_connection.cursor()
        if bill_id:
            print("Invoice ")
            cursor.execute("SELECT * FROM bills WHERE BillID = %s", (bill_id,))
            bill = cursor.fetchone()
            if bill is None:
                print("Bill not found.")
                return
            customer_id = bill[1]
            cursor.execute("SELECT * FROM customers WHERE CustomerID = %s", (customer_id,))
            customer = cursor.fetchone()
            customer_name = customer[1] + " " + customer[2]
            customer_email = customer[3]
            cursor.execute("SELECT * FROM bookings WHERE BookingID = %s", (bill[1],))
            booking = cursor.fetchone()


            print("Customer Name: ", customer_name)
            print("Customer Email: ", customer_email)
            print("Room number: ", booking[2])
            print("Check-in date: ", booking[3])
            print("Check-out date: ", booking[4])
            print("Number of guests: ", booking[5])

            print("Room Details: ")
            
            print(tabulate([booking], headers=["BookingID", "CustomerID", "RoomID", "CheckInDate", "CheckOutDate", "NumberOfGuests"], tablefmt="double_grid"))

            print("Service Details: ")
            cursor.execute("SELECT * FROM servicebookings WHERE BookingID = %s", (booking[0],))
            service_bookings = cursor.fetchall()
            if not service_bookings:
                print("No service bookings found.")
            else:
                print(tabulate(service_bookings, headers=["ServiceBookingID", "BookingID", "ServiceID", "Quantity", "TotalPrice"], tablefmt="double_grid"))
            room_cost = bill[2]
            service_cost = bill[3]
            total_amount = bill[4]

            print("Room Cost: ", room_cost)
            print("Service Cost: ", service_cost)
            print("Total Amount: ", total_amount)

            print_horizontal_line()
            return
        cursor.execute("SELECT * FROM bills")
        bills = cursor.fetchall()
        print("Bills: ")
        if not bills:
            print("No bills found.")
            return
        print(tabulate(bills, headers=["Bill ID", "Booking ID", "Room Cost", "Service Cost", "Total Amount", "Payment Status"], tablefmt="double_grid"))
        
    except mysql.connector.Error as err:
        print("Error fetching bills: {}".format(err))
    finally:
        cursor.close()
        

