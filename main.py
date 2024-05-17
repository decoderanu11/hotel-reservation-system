import os
# _here = os.path.dirname(os.path.abspath(__file__))
# filename = os.path.join(_here, '.env')
# if not os.path.isfile(filename):
#     setup()
from bills import *
from customers import *
from room import *
from bookings import *
from roomServices import *
from serviceBooking import *
from users import *

#  This is the main file that runs the program
# here we import the functions from the other files and run them in the main function


#  admin menu
user_management_menu = """
1. Add User
2. Update User
3. Delete User
4. View Users"""

booking_management_menu = """
5. View Bookings
6. Update Booking
7. Delete Booking"""

room_management_menu =    """
8. View Rooms
9. add room
10. delete room
11. update room"""

customer_management_menu ="""
12. View Customers
13. Update Customer
14. Delete Customer
15. Add Customer
"""
service_management_menu ="""
16. View Services
17. Add Service
18. Update Service
19. Delete Service
20. View Service Bookings
"""

bill_management_menu ="""
21. View Bills"""


exit_menu ="""
23. Exit
"""

staff_booking_management_menu = """
1. View Room Availability
2. Make Booking / Check-in
3. Check-out
4. Update Booking
5. Cancel Booking
6. View Bookings
"""

staff_customer_management_menu = """
7. Add Customer
8. View Customers
9. Update Customer
10. Delete Customer
"""
staff_service_management_menu = """
11. Request Room Service
12. View Room Service Bookings
13. View Available Room Services
"""

staff_bill_management_menu = """
14. View Bills
"""
def admin_menu(option: str):
    match option:
            # user management
            case "1":
                add_user()
            case "2":
                update_user()
            case "3":
                delete_user()
            case "4":
                view_users()

            # booking management
            case "5":
                view_bookings()
            case "6":
                update_booking()
            case "7":
                delete_booking()

            # room management
            case "8":
                view_rooms()
            case "9":
                add_room()
            case "10":
                delete_room()
            case "11":
                update_room()

            # customer management
            case "12":
                view_customers()
            case "13":
                update_customer()
            case "14":
                delete_customer()
            case "15":
                add_customer()
            
            # service management
            case "16":
                view_services()
            case "17":
                add_service()
            case "18":
                update_service()
            case "19":
                delete_service()
            case "20":
                view_service_bookings()

            # bill management
            case "21":
                view_bills()
                bill_id = input(" Enter the bill id to view the bill details or press enter to go back to the main menu:")
                
                if bill_id:
                    view_bills(bill_id)
            case "22":
                main()
            case "23":
                exit(1)

            case _:
                print("Invalid option.")

def staff_menu(option: str):

    match option:
        # booking management
        case "1":
            check_room_availability()
        case "2":
            print("""
            1. New Booking
            2. Check-in existing booking""")
            choice = input("Enter option: ")
            if choice == "1":
                make_booking()
            elif choice == "2":
                check_in()
            else:
                print("Invalid option.")
        case "3":
            check_out()
        case "4":
            update_booking()
        case "5":
            cancel_booking()
        case "6":
            view_bookings()

        # customer management
        case "7":
            add_customer()
        case "8":
            view_customers()
        case "9":
            update_customer()
        case "10":
            delete_customer()

        # service management
        case "11":
            make_service_booking()
        case "12":
            view_service_bookings()
        case "13":
            view_services()

        # bill management
        case "14":
            view_bills()
            bill_id = input(" Enter the bill id to view the bill details or press enter to go back to the main menu:")    
            if bill_id:
                view_bills(bill_id)
                
        case "15":
            main()

        case "16":
            exit(1)
        case _:
            print("Invalid option.")

def main():
    # here we will call the functions from the other files
    os.system('cls' if os.name == 'nt' else 'clear')
    role = user_login()
    if role.lower() == 'admin':
        while True:
            print(tabulate([[user_management_menu, booking_management_menu, room_management_menu, customer_management_menu, service_management_menu],[bill_management_menu,"22. logout",exit_menu]],
                        headers=["User Management","Booking Management","Room Management","Customer Management","Room Service Management"], tablefmt='simple_grid'))
            option = input("Enter option: ")
            if option == '23':
                exit(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            admin_menu(option)
            input("Press Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')
    else:
        while True:
            print(tabulate([[staff_booking_management_menu, staff_customer_management_menu, staff_service_management_menu ],[staff_bill_management_menu,"15. logout","16. Exit"]],
                        headers=["Booking","Customer","Room Service"], tablefmt='simple_grid'))
            option = input("Enter option: ")
            if option == '15':
                main()
            os.system('cls' if os.name == 'nt' else 'clear')
            staff_menu(option)
            input("Press Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":  
    main()