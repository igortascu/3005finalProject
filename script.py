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
    connection_parameters = "dbname='finalProject' user='postgres' host='localhost' password='Igor1999'"
   
    try:
        conn = psycopg2.connect(connection_parameters)
        print("Successfully connected to DB")
        return conn

    except psycopg2.DatabaseError as error:
        print(f"Database connection error: {error}")
        return None

'''
    Function that initializes the database with the dql and dml scripts from the directory

    parames:
        db: the database connection in order to access it and query it as user selects options
'''
def initialize_database(db):
    # Read DDL script
    with open('ddl.sql', 'r') as file:
        ddl_script = file.read()
    
    # Read DML script
    with open('dml.sql', 'r') as file:
        dml_script = file.read()

    try:
        cur = db.cursor()
        cur.execute(ddl_script)
        cur.execute(dml_script)
        db.commit()
        print("Database initialized successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
    finally:
        cur.close()

'''
    Function that clears the database and makes it ready for new test run

    parames:
        db: the database connection in order to access it and query it as user selects options
'''
def clear_database(db):
    try:
        cur = db.cursor()
        cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        db.commit()
        print("Database cleared successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error clearing database: {e}")
    finally:
        cur.close()

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
    #clear_database(db)
    #initialize_database(db)
    #main_menu(db)

if __name__ == "__main__":
    main()


# 1 TODO: modify dummy data 
# 2 TODO: finalize menu
# 3 TODO: start the queries 
# 4 TODO: double check deadline
    
    