'''
Igor Tascu
101181093

script.py - source code file for COMP 3005 Final Project V2, executes the program prompts
'''

import psycopg2
from queries import get_member_profile

'''
    Function that establishes database connection

    returns:
        connection: the databse connection object
'''
def get_db_connection():
    connection_parameters = "dbname='<USERNAME>' user='postgres' host='localhost' password='<PASSWORD>'"
   
    try:
        conn = psycopg2.connect(connection_parameters)
        return conn

    except psycopg2.DatabaseError as error:
        print(f"Database connection error: {error}")
        return None

'''
    Main menu function that prints the main menu and handles input prompts

    parames:
        db: the database connection in order to access it and query it as user selects options
'''
def main_menu(db):
    print("Welcome to the Health and Fitness Club Management System")
    print("Please select your role:")
    print("1. Member")
    print("2. Trainer")
    print("3. Admin")
    print("Q. Quit")
    
    choice = input("Enter your choice (1/2/3/Q): ").strip().upper() 
    
    if choice == '1':
        member_menu(db)
    elif choice == '2':
        trainer_menu(db)
    elif choice == '3':
        admin_menu(db)
    elif choice == 'Q':
        print("Exiting the program. Goodbye!")
        return
    else:
        print("Invalid choice. Please enter 1, 2, 3, or Q.")
        main_menu(db)

'''
    Member menu function that prints the menu for members and queries respective to their choice
    
    parames:
        db: the database connection in order to access it and query it as user selects options
'''
def member_menu(db):
    print("\n--- Member Menu ---")
    print("1. View Profile")
    print("2. Update Profile")
    print("3. Schedule a Training Session")
    print("4. Join a Group Fitness Class")
    print("5. Return to Main Menu")
    
    choice = input("Enter your choice: ")
    if choice == '5':
        main_menu(db)
    elif choice == '2':
        get_member_profile()
        

'''
    Trainer menu function that prints the menu for trainers and queries respective to their choice

    parames:
        db: the database connection in order to access it and query it as user selects options
'''
def trainer_menu(db):
    print("\n--- Trainer Menu ---")
    print("1. View Schedule")
    print("2. Set Availability")
    print("3. View Member Profiles")
    print("4. Return to Main Menu")
    
    choice = input("Enter your choice: ")
    if choice == '4':
        main_menu(db)
    else:
        print("Feature coming soon...")

'''
    Admin menu function that prints the menu for admins and queries respective to their choice

    parames:
        db: the database connection in order to access it and query it as user selects options
'''
def admin_menu(db):
    print("\n--- Admin Menu ---")
    print("1. Room Booking Management")
    print("2. Equipment Maintenance")
    print("3. Class Schedule Updates")
    print("4. Billing and Payments")
    print("5. Return to Main Menu")
    
    choice = input("Enter your choice: ")
    if choice == '5':
        main_menu(db)
    else:
        print("Feature coming soon...")

'''
    Main function for testing script
'''
def main():
    
    db = get_db_connection()
    main_menu(db)

if __name__ == "__main__":
    main()
