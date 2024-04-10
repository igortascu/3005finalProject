'''
Igor Tascu
101181093

queries.py - source code file for COMP 3005 Final Project V2, contains all the queries required 
for the program
'''

#-------------- MEMBER QUERIES ---------------#
def get_member_profile(db, email):
    try:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM Members WHERE Email = %s", (email,))
            profile = cur.fetchone()
            if profile:
                print("\n--- Member Profile ---")
                # Assuming columns are in the following order: MemberID, FirstName, LastName, Email, DateOfBirth, FitnessGoals, HealthMetrics
                print(f"Member ID: {profile[0]}")
                print(f"First Name: {profile[1]}")
                print(f"Last Name: {profile[2]}")
                print(f"Email: {profile[3]}")
                print(f"Date of Birth: {profile[4]}")
                print(f"Fitness Goals: {profile[5]}")
                print(f"Health Metrics: {profile[6]}\n")
            else:
                print("Profile not found.")
    except Exception as e:
        print(f"An error occurred while retrieving the profile: {e}")

def get_all_members(db):
    try:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM Members")
            members = cur.fetchall()
            print("\n--- All Members ---")
            for profile in members:
                # Assuming columns are in the following order: MemberID, FirstName, LastName, Email, DateOfBirth, FitnessGoals, Health Metrics
                print(f"Member ID: {profile[0]}, Name: {profile[1]} {profile[2]}, Email: {profile[3]}")
            if not members:
                print("No members found.")
    except Exception as e:
        print(f"An error occurred while retrieving all members: {e}")


def update_member_attribute(db, email, attribute, new_value):
    try:
        with db.cursor() as cur:
            # Using psycopg2's SQL module to safely create the query
            # This helps prevent SQL injection by safely creating a SQL identifier
            from psycopg2 import sql
            cur.execute(
                sql.SQL("UPDATE Members SET {} = %s WHERE Email = %s").format(
                    sql.Identifier(attribute)
                ),
                (new_value, email)
            )
            db.commit()
            print(f"{attribute} updated successfully.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")

# Print out the current schedule for member to view slots
def get_training_session_schedule(db):
    try:
        with db.cursor() as cur:
            cur.execute("SELECT SessionID, DateTime, Status, TrainerID FROM PersonalTrainingSessions WHERE Status = 'Scheduled'")
            sessions = cur.fetchall()
            print("\n--- Training Session Schedule ---")
            for session in sessions:
                print(f"Session ID: {session[0]}, DateTime: {session[1]}, Status: {session[2]}, Trainer ID: {session[3]}")
            if not sessions:
                print("No scheduled training sessions found.")
    except Exception as e:
        print(f"An error occurred while retrieving the training session schedule: {e}")
    input("Press Enter to return to the previous menu...")

def schedule_member_session(db, member_email, session_id):
    print("Scheduling Session...")
    try:
        with db.cursor() as cur:
            # Begin by checking if the session ID exists and is available
            cur.execute("SELECT Status FROM PersonalTrainingSessions WHERE SessionID = %s", (session_id,))
            session = cur.fetchone()
            if session and session[0] == 'Scheduled':
                # Update the session to be booked by the member
                cur.execute("UPDATE PersonalTrainingSessions SET MemberID = (SELECT MemberID FROM Members WHERE Email = %s), Status = 'Booked' WHERE SessionID = %s",
                            (member_email, session_id))
                db.commit()
                print(f"Training session {session_id} has been scheduled successfully for member with email {member_email}.")
            else:
                print("The session is not available for scheduling.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while scheduling the session: {e}")
    input("Press Enter to return to the previous menu...")

def get_fitness_classes_table(db):
    try:
        with db.cursor() as cur:
            cur.execute("SELECT ClassID, ClassName, DateTime, TrainerID FROM GroupFitnessClasses")
            classes = cur.fetchall()
            print("\n--- Group Fitness Classes Table ---")
            for class_info in classes:
                print(f"Class ID: {class_info[0]}, Class Name: {class_info[1]}, DateTime: {class_info[2]}, Trainer ID: {class_info[3]}")
            if not classes:
                print("No fitness classes found.")
    except Exception as e:
        print(f"An error occurred while retrieving the fitness classes: {e}")
    input("Press Enter to return to the previous menu...")

def schedule_group_fitness_session(db, member_email, class_id):
    print("Scheduling Group Fitness Session...")
    try:
        with db.cursor() as cur:
            # Check if the class exists and has available spots
            cur.execute("SELECT ClassName, DateTime FROM GroupFitnessClasses WHERE ClassID = %s", (class_id,))
            class_info = cur.fetchone()
            if class_info:
                # Insert a record into the associative table that links members to classes
                cur.execute("INSERT INTO MembersGroupClasses (MemberID, ClassID) SELECT MemberID, %s FROM Members WHERE Email = %s", (class_id, member_email))
                db.commit()
                print(f"Successfully scheduled class '{class_info[0]}' at {class_info[1]} for member with email {member_email}.")
            else:
                print("The class does not exist or is not available.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while scheduling the group fitness session: {e}")
    input("Press Enter to return to the previous menu...")

def add_member_to_fitness_class(db, member_email, class_id):
    print("Adding you to a Fitness Class...")
    try:
        with db.cursor() as cur:
            # Check if the class exists and has available spots
            cur.execute("SELECT ClassName, DateTime FROM GroupFitnessClasses WHERE ClassID = %s", (class_id,))
            class_info = cur.fetchone()
            if class_info:
                # Insert a record into the associative table that links members to classes
                cur.execute("INSERT INTO MembersGroupClasses (MemberID, ClassID) SELECT MemberID, %s FROM Members WHERE Email = %s", (class_id, member_email))
                db.commit()
                print(f"You have been added to the class '{class_info[0]}' at {class_info[1]}.")
            else:
                print("The class does not exist or is not available.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while adding you to the fitness class: {e}")
    input("Press Enter to return to the previous menu...")

#-------------- TRAINER QUERIES ---------------#
def get_trainer_schedule(db):
    print("Retrieving Schedule...")
    return

def set_trainer_availability(db):
    print("Setting Availability...")
    return

def get_trainers_members(db):
    print("Retrieving Your Client's Profiles...")
    return

#-------------- ADMIN QUERIES ---------------#
def get_rooms():
    return

def get_equipment_table(db):
    print("Retrieving equipment table...")

def update_equipment_maintenance_date(db, equipment_id, new_date):
    print(f"Updating maintenance date for equipment ID {equipment_id} to {new_date}...")
    # TODO: Implement the SQL UPDATE query to set the new maintenance date

def add_equipment(db, equipment_name, maintenance_date):
    print(f"Adding new equipment {equipment_name} with maintenance date {maintenance_date}...")
    # TODO: Implement the SQL INSERT query to add new equipment

def remove_equipment(db, equipment_id):
    print(f"Removing equipment ID {equipment_id}...")
    # TODO: Implement the SQL DELETE query to remove equipment

def update_class_schedule(db, class_id, new_datetime):
    print(f"Updating schedule for class ID {class_id} to {new_datetime}...")
    # TODO: Implement the SQL UPDATE query to set the new schedule

def add_class_schedule(db, class_name, datetime, trainer_id, room_id):
    print(f"Adding new class {class_name} scheduled for {datetime}...")
    # TODO: Implement the SQL INSERT query to add a new class schedule

def remove_class_schedule(db, class_id):
    print(f"Removing class ID {class_id} from schedule...")
    # TODO: Implement the SQL DELETE query to remove a class from the schedule

def process_billing(db, member_id, amount, date, status):
    print(f"Processing billing for member ID {member_id}: Amount: {amount}, Date: {date}, Status: {status}...")
    # TODO: Implement the SQL INSERT/UPDATE query to process billing information