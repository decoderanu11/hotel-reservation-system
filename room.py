from db import get_db_connection
import mysql.connector
from tabulate import tabulate

db_connection = get_db_connection()

def add_room():
    try:
        cursor = db_connection.cursor()

        room_type = input("Enter room type: ")
        price = float(input("Enter room price: "))
        status = input("Enter room status Available/Unavailable: ")

        # Insert data into the table
        cursor.execute("""
            INSERT INTO Rooms (RoomType, Price, Status) 
            VALUES (%s, %s, %s)
        """, (room_type, price, status))
        
        db_connection.commit()

        print("Room added successfully.")
        view_rooms()
    except mysql.connector.Error as err:
        print("Error adding room: {}".format(err))
    finally:
        cursor.close()

def update_room():
    try:
        view_rooms()
        cursor = db_connection.cursor()

        room_id = input("Enter Room ID to update: ")
        room_type = input("Enter new room type: ")
        price = float(input("Enter new room price: "))
        status = input("Enter new room status: ")

        # Update room details
        cursor.execute("""
            UPDATE Rooms 
            SET RoomType = %s, Price = %s, Status = %s
            WHERE RoomID = %s
        """, (room_type, price, status, room_id))
        
        db_connection.commit()

        print("Room details updated successfully.")
        view_rooms()
    except mysql.connector.Error as err:
        print("Error updating room: {}".format(err))
    finally:
        cursor.close()

def delete_room():
    try:
        view_rooms()
        cursor = db_connection.cursor()

        room_id = input("Enter Room ID to delete: ")

        # Delete room details
        cursor.execute("""
            DELETE FROM Rooms 
            WHERE RoomID = %s
        """, (room_id,))
        
        db_connection.commit()

        print("Room deleted successfully.")
        view_rooms()
    except mysql.connector.Error as err:
        print("Error deleting room: {}".format(err))
    finally:
        cursor.close()

def view_rooms():
    try:
        cursor = db_connection.cursor()

        cursor.execute("SELECT * FROM Rooms")
        rooms = cursor.fetchall()
        if not rooms:
            print("No rooms available.")
            return
        print(tabulate(rooms, headers=["Room ID", "Room Type", "Price", "Status"], tablefmt="double_grid"))

        # mydata = []
        # for room in rooms:
        #     mydata.append([room[0], room[1], room[2], room[3]])
        # print(tabulate(mydata, headers=["Room ID", "Room Type", "Price", "Status"]))
        # for room in rooms:
        #     print(room)
    except mysql.connector.Error as err:
        print("Error fetching rooms: {}".format(err))
    finally:
        cursor.close()