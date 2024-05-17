import time
import mysql.connector
from dotenv import load_dotenv
import os
import pickle
import os.path
from dotenv import set_key
from pathlib import Path


env_file_path = Path(".env")
# Create the file if it does not exist.

# Save some values to the file.
# load_dotenv()  


def setup():
    print("Setting up...")
    print("please fill data carefully")
    print("Case sensitive")
    print("Enter the following details")
    dbhost = input("Enter Database host: ")
    dbuser = input("Enter Database username: ")
    dbpass = input("Enter Database password: ")
    mydb = mysql.connector.connect(
            host=dbhost,
            user=dbuser,
            password=dbpass
            )


    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS hotel_reservation_system")
    mydb.commit()
    mycursor.close()

    mydb = mysql.connector.connect(
            host=dbhost,
            user=dbuser,
            password=dbpass,
            database="hotel_reservation_system"
            )
    mycursor = mydb.cursor()
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Customers (CustomerID INT PRIMARY KEY AUTO_INCREMENT,
                        FirstName VARCHAR(100),
                        LastName VARCHAR(100),
                        Email VARCHAR(100),
                        Phone VARCHAR(15),
                        Address VARCHAR(255))"""
                    )
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                       UserID INT PRIMARY KEY AUTO_INCREMENT,
                        Username VARCHAR(50) UNIQUE,
                        Password VARCHAR(50),
                        Role VARCHAR(50))"""
                    )
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Rooms (
                        RoomID INT PRIMARY KEY AUTO_INCREMENT,
                        RoomType VARCHAR(50),
                        Price DECIMAL(10, 2),
                        Status VARCHAR(50))"""
                    )
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Services (
                        ServiceID INT PRIMARY KEY AUTO_INCREMENT,
                        ServiceName VARCHAR(100),
                        Price DECIMAL(10, 2))"""
                    )
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Bookings (
                        BookingID INT PRIMARY KEY AUTO_INCREMENT,
                        CustomerID INT,
                        RoomID INT,
                        CheckInDate DATE,
                        CheckOutDate DATE,
                        NumberOfGuests INT,
                        Status VARCHAR(50),
                        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE SET NULL ON UPDATE SET NULL,
                        FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID) ON DELETE SET NULL ON UPDATE SET NULL)"""
                    )
    mycursor.execute("""CREATE TABLE IF NOT EXISTS ServiceBookings (
                        ServiceBookingID INT PRIMARY KEY AUTO_INCREMENT,
                        BookingID INT,
                        ServiceID INT,
                        Quantity INT,
                        TotalPrice DECIMAL(10, 2),
                        FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID) ON DELETE SET NULL ON UPDATE SET NULL,
                        FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID) ON DELETE SET NULL ON UPDATE SET NULL)"""
                    )
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Bills (
                        BillID INT PRIMARY KEY AUTO_INCREMENT,
                        BookingID INT,
                        RoomCost DECIMAL(10, 2),
                        ServiceCost DECIMAL(10, 2),
                        TotalAmount DECIMAL(10, 2),
                        PaymentStatus VARCHAR(50),
                        FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID) ON DELETE SET NULL ON UPDATE SET NULL)"""
                    )
    mydb.commit()
    
    print("database created successfully")
    username = input("create admin username for application: ")
    password = input("create admin password for application: ")
    role = 'admin'
    try:
        mycursor.execute("INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)", (username, password, role))
    except Exception as e:
        pass
    try:
        mycursor.execute("INSERT INTO Rooms (RoomType, Price, Status) VALUES ('Single', 1500, 'Available')")
        mycursor.execute("INSERT INTO Rooms (RoomType, Price, Status) VALUES ('Double', 2200, 'Available')")
        mycursor.execute("INSERT INTO Rooms (RoomType, Price, Status) VALUES ('Suite', 3000, 'Available')")
        mycursor.execute("INSERT INTO Services (ServiceName, Price) VALUES ('Breakfast', 200)")
        mycursor.execute("INSERT INTO Services (ServiceName, Price) VALUES ('Lunch', 300)")
        mycursor.execute("INSERT INTO Services (ServiceName, Price) VALUES ('Dinner', 400)")
        mycursor.execute("INSERT INTO Customers (FirstName, LastName, Email, Phone, Address) VALUES ('Anurag', 'Sharma', 'xyz@g.c', '1111', 'xyz,India')")
        mycursor.execute("INSERT INTO Customers (FirstName, LastName, Email, Phone, Address) VALUES ('Rahul', 'Sharma', 'abc@g.c', '2222', 'abc,India')")
    except Exception as e:
        pass

    mydb.commit()
    print("Admin created successfully")
    print("Setup complete")
    # with open(".env", "w") as f:
    #     f.write('DB_USER="'+dbuser+'"\n')
    #     f.write('DB_HOST="'+dbhost+'"\n')
    #     f.write('DB_PASSWORD="'+dbpass+'"\n')
    #     f.write('DB_NAME="hotel_reservation_system"\n')
    try:
        env_file_path.touch(mode=0o600, exist_ok=False)
    except Exception as e:
        pass
    set_key(dotenv_path=env_file_path, key_to_set="DB_USER", value_to_set=dbuser)
    set_key(dotenv_path=env_file_path, key_to_set="DB_HOST", value_to_set=dbhost)
    set_key(dotenv_path=env_file_path, key_to_set="DB_PASSWORD", value_to_set=dbpass)
    set_key(dotenv_path=env_file_path, key_to_set="DB_NAME", value_to_set="hotel_reservation_system")
    print("Environment variables set successfully")
    print("Please run the application again")
    print("Thank you")
    print("Exiting...")
    time.sleep(2)
    exit(0)

setup()

