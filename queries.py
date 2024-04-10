'''
Igor Tascu
101181093

queries.py - source code file for COMP 3005 Final Project V2, contains all the queries required 
for the program
'''


#-------------- MEMBER QUERIES ---------------#
def get_member_profile(db):
    print("Retrieving Profile...")
    return

def udpate_member_profile(db):
    print("Updating Profile...")
    return

def get_all_members(db):
    return

# Print out the current schedule for member to view slots
def get_training_session_schedule():
    return

def schedule_member_session(db, session_choice):
    print("Scheduling Session...")
    return


def get_fitness_classes_table(db):
    return

def schedule_group_fitness_session(db, session_choice):
    print("Scheduling Session...")
    return

def add_member_to_fitness_class(db):
    print("Adding you to a Fitness Class...")
    return

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