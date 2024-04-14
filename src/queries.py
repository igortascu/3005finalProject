'''
Igor Tascu
101181093

queries.py - source code file for COMP 3005 Final Project V2, contains all the queries required 
for the program
'''
from script import validate_email
from psycopg2 import sql
import json

#-------------- MEMBER QUERIES ---------------#
def get_member_profile(db, email):
    try:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM Members WHERE Email = %s", (email,))
            profile = cur.fetchone()
            if profile:
                print("\n--- Member Profile ---")
                print(f"Member ID: {profile[0]}")
                print(f"First Name: {profile[1]}")
                print(f"Last Name: {profile[2]}")
                print(f"Email: {profile[3]}")
                print(f"Date of Birth: {profile[5]}")
                print(f"Fitness Goals: {profile[6]}")
                print(f"Health Metrics: {profile[7]}\n")
            else:
                print("Profile not found.")
    except Exception as e:
        print(f"An error occurred while retrieving the profile: {e}")

def register_user(db):
    print("Welcome to our Gym! Here is the sign up form!")
    email = input("Email: ")
    if not validate_email(email):
        print("Invalid email format. Please try again.")
        return
    password = input("Password: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    date_of_birth = input("Date of Birth (YYYY-MM-DD): ")
    fitness_goals = " "
    health_metrics = " "

    # Insert new member into the DB
    try:
        with db.cursor() as cur:
            cur.execute("""
                INSERT INTO Members (FirstName, LastName, Email, Password, DateOfBirth, FitnessGoals, HealthMetrics) 
                VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')), %s, %s, %s)
            """, (first_name, last_name, email, password, date_of_birth, fitness_goals, health_metrics))
            db.commit()
            print("Your account has been created!")
            
            # Process initial payment
            amount = float(input("Initial Payment Amount ($): "))
            payment_status = 'Paid'
            cur.execute("""
                INSERT INTO Billing (MemberID, Amount, Date, PaymentStatus) 
                VALUES ((SELECT MemberID FROM Members WHERE Email = %s), %s, CURRENT_DATE, %s)
            """, (email, amount, payment_status))
            db.commit()
            print("Your payment has been processed. Welcome to the gym!")
            return email
            
    except Exception as e:
        db.rollback()
        print(f"An error occurred while creating your account: {e}")
        return False

def get_all_members(db):
    try:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM Members")
            members = cur.fetchall()
            print("\n--- All Members ---")
            for profile in members:
                print(f"Member ID: {profile[0]}, Name: {profile[1]} {profile[2]}, Email: {profile[3]}")
            if not members:
                print("No members found.")
    except Exception as e:
        print(f"An error occurred while retrieving all members: {e}")

def update_member_attribute(db, email, attribute, new_value):
    attribute = attribute.lower()
    try:
        with db.cursor() as cur:
            cur.execute(
                sql.SQL("UPDATE members SET {} = %s WHERE email = %s").format(
                    sql.Identifier(attribute)
                ),
                (new_value, email)
            )
            if cur.rowcount:
                db.commit()
                print(f"{attribute} updated successfully.")
            else:
                print("The attribute was not updated. Please check if the email is correct.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")


# Print out the current schedule for member to view slots
def get_training_session_schedule(db):
    try:
        with db.cursor() as cur:
            # Select all trainers and their availability status
            cur.execute("""
                SELECT TrainerID, FirstName, LastName, Availability, IsAvailable
                FROM Trainers
                WHERE IsAvailable = TRUE
                ORDER BY LastName, FirstName;
            """)
            trainers = cur.fetchall()
            print("\n--- Trainer Availability ---")
            for trainer in trainers:
                trainer_name = f"{trainer[1]} {trainer[2]}"
                available_times = trainer[3]  # Assuming this is a JSON string or similar
                available = 'Available' if trainer[4] else 'Not Available'
                print(f"Trainer: {trainer_name}, Availability: {available_times}, Status: {available}")
            if not trainers:
                print("No trainers are currently available.")
    except Exception as e:
        print(f"An error occurred while retrieving the trainers' availability: {e}")

def schedule_member_session(db, member_email, trainer_id):
    print("Scheduling Personal Training Session...")
    try:
        with db.cursor() as cur:
            # Fetch the trainer's next available time
            cur.execute("""
                SELECT Availability FROM Trainers
                WHERE TrainerID = %s AND IsAvailable = TRUE;
            """, (trainer_id,))
            availability = cur.fetchone()
            if availability:
                # Schedule the session using the trainer's next available time
                cur.execute("""
                    SELECT MemberID FROM Members
                    WHERE Email = %s;
                """, (member_email,))
                member = cur.fetchone()
                if member:
                    member_id = member[0]
                    # Book the session by creating a record in PersonalTrainingSessions
                    cur.execute("""
                        INSERT INTO PersonalTrainingSessions (MemberID, TrainerID, ScheduledTime, Status)
                        VALUES (%s, %s, %s, 'Booked');
                    """, (member_id, trainer_id, availability[0]))
                    # Optionally, update the trainer's availability
                    cur.execute("""
                        UPDATE Trainers
                        SET IsAvailable = FALSE
                        WHERE TrainerID = %s;
                    """, (trainer_id,))
                    db.commit()
                    print(f"Personal training session has been scheduled with trainer ID {trainer_id} for member with email {member_email} at {availability[0]}.")
                else:
                    print("Member email not found.")
            else:
                print("The selected trainer is not available or does not exist.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while scheduling the session: {e}")
    input("Press Enter to return to the previous menu...")

def get_fitness_classes_table(db):
    try:
        with db.cursor() as cur:
            cur.execute("""
                SELECT gfc.ClassID, gfc.ClassName, gfc.DateTime, t.FirstName, t.LastName
                FROM GroupFitnessClasses gfc
                JOIN Trainers t ON gfc.TrainerID = t.TrainerID
                ORDER BY gfc.DateTime;
            """)
            classes = cur.fetchall()
            print("\n--- Group Fitness Classes Table ---")
            for class_info in classes:
                trainer_name = f"{class_info[3]} {class_info[4]}"
                print(f"Class ID: {class_info[0]}, Class Name: {class_info[1]}, DateTime: {class_info[2]}, Trainer: {trainer_name}")
            if not classes:
                print("No fitness classes found.")
    except Exception as e:
        print(f"An error occurred while retrieving the fitness classes: {e}")

def register_for_fitness_class(db, member_email, class_id):
    print("Registering for a Fitness Class...")
    try:
        with db.cursor() as cur:
            # Check if the class exists
            cur.execute("""
                SELECT ClassName, DateTime, t.FirstName, t.LastName
                FROM GroupFitnessClasses gfc
                JOIN Trainers t ON gfc.TrainerID = t.TrainerID
                WHERE gfc.ClassID = %s;
            """, (class_id,))
            class_info = cur.fetchone()
            if class_info:
                # Insert a record into the associative table that links members to classes
                cur.execute("""
                    INSERT INTO MembersGroupClasses (MemberID, ClassID)
                    SELECT MemberID, %s FROM Members WHERE Email = %s;
                """, (class_id, member_email))
                db.commit()
                trainer_name = f"{class_info[2]} {class_info[3]}"
                print(f"You have been registered for the class '{class_info[0]}' with {trainer_name} at {class_info[1]}.")
            else:
                print("The class does not exist or registration is not available.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while registering for the fitness class: {e}")
    input("Press Enter to continue...")


#-------------- TRAINER QUERIES ---------------#
def get_trainer_schedule(db, trainer_id):
    try:
        with db.cursor() as cur:
            # Get the booked sessions.
            cur.execute("""
                SELECT ts.SessionID, ts.ScheduledTime, ts.Status, m.FirstName, m.LastName 
                FROM PersonalTrainingSessions ts
                JOIN Members m ON ts.MemberID = m.MemberID
                WHERE ts.TrainerID = %s AND ts.Status = 'Booked'
                ORDER BY ts.ScheduledTime;
            """, (trainer_id,))
            sessions = cur.fetchall()
            
            # Now get the trainer's next available time.
            cur.execute("""
                SELECT Availability FROM Trainers
                WHERE TrainerID = %s;
            """, (trainer_id,))
            next_available = cur.fetchone()

            print("\n--- Trainer Schedule ---")
            
            if sessions:
                for session in sessions:
                    print(f"Session ID: {session[0]}, Scheduled Time: {session[1]}, Status: {session[2]}, Member: {session[3]} {session[4]}")
            else:
                print("No booked sessions found for this trainer.")
            
            if next_available:
                print(f"Next Available Time: {next_available[0]}")
            else:
                print("No availability information found for this trainer.")
                
    except Exception as e:
        print(f"An error occurred while retrieving the trainer's schedule: {e}")


def set_trainer_availability(db, trainer_id, new_availability):
    try:
        with db.cursor() as cur:
            # Assuming new_availability is a string representing the trainer's new available timestamp, e.g., '2024-04-20 09:00:00'
            cur.execute("""
                UPDATE Trainers
                SET Availability = %s, IsAvailable = TRUE
                WHERE TrainerID = %s;
            """, (new_availability, trainer_id))
            db.commit()
            print("Trainer's availability updated successfully.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while setting the trainer's availability: {e}")

def get_trainers_members(db, trainer_id):
    try:
        with db.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT m.MemberID, m.FirstName, m.LastName, m.Email 
                FROM Members m
                JOIN PersonalTrainingSessions ts ON m.MemberID = ts.MemberID
                WHERE ts.TrainerID = %s AND ts.Status = 'Booked';
            """, (trainer_id,))
            members = cur.fetchall()
            print("\n--- Trainer's Clients ---")
            for member in members:
                print(f"Member ID: {member[0]}, Name: {member[1]} {member[2]}, Email: {member[3]}")
            if not members:
                print("No members currently booked with this trainer.")
    except Exception as e:
        print(f"An error occurred while retrieving the trainer's clients: {e}")

#-------------- ADMIN QUERIES ---------------#
def get_rooms(db):
    try:
        with db.cursor() as cur:
            cur.execute("SELECT RoomID, RoomName, Capacity FROM Rooms ORDER BY RoomName;")
            rooms = cur.fetchall()
            print("\n--- Rooms List ---")
            for room in rooms:
                print(f"Room ID: {room[0]}, Name: {room[1]}, Capacity: {room[2]}")
            if not rooms:
                print("No rooms found.")
    except Exception as e:
        print(f"An error occurred while retrieving rooms: {e}")
    input("Press Enter to return to the previous menu...")

def get_equipment_table(db):
    print("Retrieving equipment table...")
    try:
        with db.cursor() as cur:
            cur.execute("SELECT EquipmentID, EquipmentName, MaintenanceDate FROM Equipment ORDER BY EquipmentName;")
            equipment = cur.fetchall()
            print("\n--- Equipment Table ---")
            for item in equipment:
                print(f"Equipment ID: {item[0]}, Name: {item[1]}, Maintenance Date: {item[2]}")
            if not equipment:
                print("No equipment found.")
    except Exception as e:
        print(f"An error occurred while retrieving equipment: {e}")

def update_equipment_maintenance_date(db, equipment_id, new_date):
    print(f"Updating maintenance date for equipment ID {equipment_id} to {new_date}...")
    try:
        with db.cursor() as cur:
            cur.execute("UPDATE Equipment SET MaintenanceDate = %s WHERE EquipmentID = %s", (new_date, equipment_id))
            if cur.rowcount == 0:
                print(f"No equipment found with ID {equipment_id}.")
            else:
                db.commit()
                print(f"Equipment ID {equipment_id} maintenance date updated to {new_date}.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while updating the maintenance date: {e}")
    input("Press Enter to return to the previous menu...")

def add_equipment(db, equipment_name, maintenance_date):
    print(f"Adding new equipment {equipment_name} with maintenance date {maintenance_date}...")
    try:
        with db.cursor() as cur:
            cur.execute("INSERT INTO Equipment (EquipmentName, MaintenanceDate) VALUES (%s, %s)", (equipment_name, maintenance_date))
            db.commit()
            print(f"New equipment '{equipment_name}' added with maintenance date {maintenance_date}.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while adding new equipment: {e}")
    input("Press Enter to return to the previous menu...")

def remove_equipment(db, equipment_id):
    try:
        with db.cursor() as cur:
            cur.execute("DELETE FROM Equipment WHERE EquipmentID = %s", (equipment_id,))
            if cur.rowcount:
                db.commit()
                print(f"Equipment ID {equipment_id} has been removed.")
            else:
                print("No equipment found with the specified ID.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while removing equipment: {e}")

def get_class_schedules(db):
    try:
        with db.cursor() as cur:
            cur.execute("""
                SELECT ClassID, ClassName, DateTime, TrainerID, RoomID FROM GroupFitnessClasses
                ORDER BY DateTime;
            """)
            classes = cur.fetchall()
            print("\n--- Current Class Schedules ---")
            for cls in classes:
                print(f"Class ID: {cls[0]}, Name: {cls[1]}, Date and Time: {cls[2]}, Trainer ID: {cls[3]}, Room ID: {cls[4]}")
            if not classes:
                print("No class schedules found.")
    except Exception as e:
        print(f"An error occurred while retrieving class schedules: {e}")

def update_class_schedule(db, class_id, new_datetime):
    try:
        with db.cursor() as cur:
            cur.execute("UPDATE GroupFitnessClasses SET DateTime = %s WHERE ClassID = %s", (new_datetime, class_id))
            if cur.rowcount:
                db.commit()
                print(f"Class schedule for ID {class_id} updated to {new_datetime}.")
            else:
                print("No class found with the specified ID or no changes made.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while updating the class schedule: {e}")

def add_class_schedule(db, class_name, datetime, trainer_id, room_id):
    try:
        with db.cursor() as cur:
            cur.execute("""
                INSERT INTO GroupFitnessClasses (ClassName, DateTime, TrainerID, RoomID)
                VALUES (%s, %s, %s, %s)
            """, (class_name, datetime, trainer_id, room_id))
            db.commit()
            print(f"New class '{class_name}' scheduled for {datetime}.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while adding the new class schedule: {e}")

def remove_class_schedule(db, class_id):
    try:
        with db.cursor() as cur:
            cur.execute("DELETE FROM GroupFitnessClasses WHERE ClassID = %s", (class_id,))
            if cur.rowcount:
                db.commit()
                print(f"Class ID {class_id} has been removed from the schedule.")
            else:
                print("No class found with the specified ID.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while removiqng the class from the schedule: {e}")

def process_billing(db, member_id, amount, date, status):
    try:
        with db.cursor() as cur:
            # Check if there's an existing record for that date.
            cur.execute("""
                SELECT BillID FROM Billing 
                WHERE MemberID = %s AND Date = %s;
            """, (member_id, date))
            bill_record = cur.fetchone()

            if bill_record:
                # Update the existing record.
                cur.execute("""
                    UPDATE Billing SET Amount = %s, PaymentStatus = %s
                    WHERE MemberID = %s AND Date = %s;
                """, (amount, status, member_id, date))
            else:
                # Insert a new record if one does not exist.
                cur.execute("""
                    INSERT INTO Billing (MemberID, Amount, Date, PaymentStatus)
                    VALUES (%s, %s, %s, %s);
                """, (member_id, amount, date, status))
            db.commit()
            print(f"Billing record updated for member ID {member_id}: Amount: {amount}, Date: {date}, Status: {status}.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while processing billing: {e}")
