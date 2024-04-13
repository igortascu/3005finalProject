'''
Igor Tascu
101181093

script.py - source code file for COMP 3005 Final Project V2, executes the program prompts
'''

import psycopg2
import re
import getpass
from datetime import datetime
from queries import *

# ------------------------------ DB INITIALIZATION FUNCTIONS ------------------------------#

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
    with open('../SQL/ddl.sql', 'r') as file:
        ddl_script = file.read()
    
    # Read DML script
    with open('../SQL/dml.sql', 'r') as file:
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

# ---------------------------------- HELPER FUNCTIONS ----------------------------------#
def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def is_valid_id(id_str):
    if not id_str.isdigit():
        return False
    id_val = int(id_str)
    return id_val > 0

def validate_email(email):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(email_regex, email)

# ------------------------------ MENU CLI FUNCTIONS ------------------------------#
'''
    Main menu function that prints the main menu and handles input prompts

    parames:
        db: the database connection in order to access it and query it as user selects options
'''

def main_menu(db):

    while True:
        print("Welcome to the Health and Fitness Club Management System")
        print("Please select your role:")
        print("1. Member")
        print("2. Trainer")
        print("3. Admin")
        print("Q. Quit")
        
        choice = input("Enter your choice (1/2/3/Q): ").strip().upper() 
        
        if choice == '1':
            user_login(db)
        elif choice == '2':
            trainer_login(db)
        elif choice == '3':
            admin_login(db)
        elif choice == 'Q':
            print("Exiting the application.")
            return
        else:
            print("Invalid choice. Please enter 1, 2, 3, or Q.")


'''
    User login function that promts user for details and logs them in
    
    parames:
        db: the database connection in order to access it and query it as user selects options
'''
def login_user(db):
    email = input("Email: ").strip()
    # Hide password input for security
    password = getpass.getpass("Password: ")

    try:
        with db.cursor() as cur:
            # Check if the email exists and the password matches
            cur.execute("""
                SELECT Email FROM Members
                WHERE Email = %s AND Password = crypt(%s, Password);
            """, (email, password))
            result = cur.fetchone()
            if result:
                print("Login successful!")
                return email
            else:
                print("Login failed. Please check your credentials and try again.")
                return None
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return None

'''
    User login function that either registers or signs in a user
    
    parames:
        db: the database connection in order to access it and query it as user selects options
'''
def user_login(db):
    print("Are you a returning or new member?")
    print("1. Returning Member")
    print("2. New Member")
    member_status = int(input("Status: "))

    if member_status == 1:
        member_email = login_user(db)
        if member_email:
            member_menu(db, member_email)
    else:
        print("Welcome to our Gym! Enter your email and password to create an account!")
        member_email = register_user(db)

        if member_email:
            # Log the new member in after successful registration
            member_menu(db, member_email)
        else:
            print("Registration failed")

'''
    Trainer login function that logs in the trainer staff
    
    parames:
        db: the database connection in order to access it and query it as user selects options
'''
def trainer_login(db):
    print("\n--- Trainer Login ---")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    try:
        with db.cursor() as cur:
            cur.execute("""
                SELECT TrainerID, FirstName, LastName FROM Trainers
                WHERE Email = %s AND Password = crypt(%s, Password);
            """, (email, password))
            trainer = cur.fetchone()
            if trainer:
                print(f"Welcome {trainer[1]} {trainer[2]}!")
                # get id
                id = 0
                trainer_menu(db, id)
            else:
                print("Invalid login credentials.")
    except Exception as e:
        print(f"An error occurred during login: {e}")

'''
    Admin login function that logs in the admin staff
    
    parames:
        db: the database connection in order to access it and query it as user selects options
'''
def admin_login(db):
    print("\n--- Admin Login ---")
    email = input("Enter your email: ")
    password = input("Enter your password: ")  # In a real system, this would be hashed

    try:
        with db.cursor() as cur:
            cur.execute("""
                SELECT StaffID, FirstName, LastName FROM AdministrativeStaff
                WHERE Email = %s AND Password = crypt(%s, Password);
            """, (email, password))
            admin = cur.fetchone()
            if admin:
                print(f"Welcome {admin[1]} {admin[2]}!")
                admin_menu(db)
            else:
                print("Invalid login credentials.")
    except Exception as e:
        print(f"An error occurred during login: {e}")


'''
    Profile management function to handle user profile change requests
    
    parames:
        db: the database connection in order to access it and query it as user selects options
'''
def profile_management(db, email):
    print("\n--- Profile Management ---")

    print("Which attribute would you like to update?")
    print("1. First Name")
    print("2. Last Name")
    print("3. Date of Birth")
    print("4. Fitness Goals")
    print("5. Health Metrics")
    attribute_choice = input("Enter the number of the attribute you want to update: ").strip()
    
    attribute_map = {
        '1': 'FirstName',
        '2': 'LastName',
        '3': 'DateOfBirth',
        '4': 'FitnessGoals',
        '5': 'HealthMetrics'
    }

    if attribute_choice in attribute_map:
        new_value = input(f"Enter the new value for {attribute_map[attribute_choice]}: ").strip()
        update_member_attribute(db, email, attribute_map[attribute_choice], new_value)
    else:
        print("Invalid choice. Please enter a number between 1-5.")
    
    input("Press Enter to return to the Member Menu...")

'''
    Member menu function that prints the menu for members and queries respective to their choice
    
    parames:
        db: the database connection in order to access it and query it as user selects options
'''
def member_menu(db, member_email):
    print("WELCOME!")
    
    while True:
        print("\n--- Member Menu ---")
        print("1. View Profile")
        print("2. Update Profile")
        print("3. Schedule a Training Session")
        print("4. Join a Group Fitness Class")
        print("5. Return to Main Menu")
        
        choice = input("Enter your choice: ")
        if choice == '5':
            main_menu(db)
        elif choice == '1':
            get_member_profile(db, member_email)
        elif choice == '2':
            profile_management(db, member_email)
        elif choice == '3':
            get_training_session_schedule(db)
            try:
                trainer_choice = int(input("From the available trainers, pick the ID of a trainer you would like to book: "))
                schedule_member_session(db, member_email, trainer_choice)
            except ValueError:
                print("Invalid input. Please enter a numeric trainer ID.")
        elif choice == '4':
            get_fitness_classes_table(db)
            session_choice = int(input("From the available sessions, pick a slot ID you would like: "))
            register_for_fitness_class(db, member_email, session_choice)

'''
    Trainer menu function that prints the menu for trainers and queries respective to their choice

    parames:
        db: the database connection in order to access it and query it as user selects options
'''
def trainer_menu(db, id):
    while True:
        print("\n--- Trainer Menu ---")
        print("1. View Schedule")
        print("2. Set Availability")
        print("3. View Member Profiles")
        print("4. Return to Main Menu")
        
        choice = input("Enter your choice: ")
        if choice == '4':
            main_menu(db)
        elif choice == '1':
            get_trainer_schedule(db, id)
        elif choice == '2':
            availabilty = input("Set the time you are available for in (DAY, TIME) format")
            set_trainer_availability(db, id, availabilty)
        elif choice == '3':
            get_all_members(db)
        
'''
    Admin menu function that prints the menu for admins and queries respective to their choice

    parames:
        db: the database connection in order to access it and query it as user selects options
'''
def admin_menu(db):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Room Booking Management")
        print("2. Equipment Maintenance")
        print("3. Class Schedule Updates")
        print("4. Billing and Payments")
        print("5. Return to Main Menu")
        
        choice = input("Enter your choice: ")
        if choice == '5':
            main_menu(db)
        elif choice == '1':
            get_rooms(db)
        elif choice == '2':
            get_equipment_table(db)

            while True:
                print("\n--- What would you like to update ---")
                print("1. Update maintance date")
                print("2. Add equipment")
                print("3. Remove equipment")
                print("4. Go back")

                maintenance_choice = input("Enter your choice: ")

                if maintenance_choice == '4':
                    admin_menu(db)
                elif maintenance_choice == '1':
                    while True:
                        equipment_id = int(input("Enter the equipment ID number to update: "))
                        new_date = input("Enter the new maintanance check up date")
                        
                        if is_valid_date(new_date):
                            update_equipment_maintenance_date(db, equipment_id, new_date)
                            break
                        else:
                            print("Date invalid try again")
                elif maintenance_choice == '2':
                    equipment_name = input("Enter the name of the new equipment: ")
                    maintenance_date = input("Enter the maintenance date for the new equipment (YYYY-MM-DD): ")
                    add_equipment(db, equipment_name, maintenance_date)
                elif maintenance_choice == '3':
                    equipment_id = int(input("Enter the equipment ID number to remove: "))
                    remove_equipment(db, equipment_id)
        
        elif choice == '3':
            while True:
                print("\n--- Class Schedule Updates ---")
                print("1. Update a Class Schedule")
                print("2. Add a New Class Schedule")
                print("3. Remove a Class from Schedule")
                print("4. Go back")

                schedule_choice = input("Enter your choice: ")

                if schedule_choice == '4':
                    break
                elif schedule_choice == '1':
                    class_id = int(input("Enter the class ID to update the schedule: "))
                    new_datetime = input("Enter the new date and time for the class (YYYY-MM-DD HH:MM): ")
                    update_class_schedule(db, class_id, new_datetime)
                elif schedule_choice == '2':
                    class_name = input("Enter the name of the new class: ")
                    datetime = input("Enter the date and time for the new class (YYYY-MM-DD HH:MM): ")
                    trainer_id = int(input("Enter the trainer ID for the class: "))
                    room_id = int(input("Enter the room ID for the class: "))
                    add_class_schedule(db, class_name, datetime, trainer_id, room_id)
                elif schedule_choice == '3':
                    class_id = int(input("Enter the class ID to remove from the schedule: "))
                    remove_class_schedule(db, class_id)
        elif choice == '4':
            while True:
                print("\n--- Billing and Payments ---")
                print("1. Process a Billing Transaction")
                print("2. Go back")

                billing_choice = input("Enter your choice: ")

                if billing_choice == '2':
                    break
                elif billing_choice == '1':
                    member_id = int(input("Enter the member ID to process the billing: "))
                    amount = float(input("Enter the billing amount: "))
                    date = input("Enter the billing date (YYYY-MM-DD): ")
                    status = input("Enter the billing status (Paid/Unpaid): ")
                    process_billing(db, member_id, amount, date, status)

'''
    Main function for testing script
'''
def main():
    
    db = get_db_connection()
    clear_database(db)
    initialize_database(db)
    main_menu(db)

if __name__ == "__main__":
    main()
