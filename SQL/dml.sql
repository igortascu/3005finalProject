-- Inserting into Members
INSERT INTO Members (FirstName, LastName, Email, Password, DateOfBirth, FitnessGoals, HealthMetrics)
VALUES 
('Igor', 'Tascu', 'igortascu@gmail.com', crypt('Igor1999', gen_salt('bf')), '2002-09-10', '{"weightTarget":"180lbs","timeTarget":"3mo"}', '{"currentWeight":"155lbs","heartRate":"50bpm"}'),
('Jane', 'Smith', 'jane.smith@gmail.com', crypt('Jane2931', gen_salt('bf')), '1990-07-22', '{"weightTarget":"130lbs"}', '{"currentWeight":"150lbs","heartRate":"80bpm"}');

-- Assuming you are using a specific day for the schedule, replace 'YYYY-MM-DD' with the actual date
INSERT INTO Trainers (FirstName, LastName, Email, Password, Availability, IsAvailable)
VALUES 
('Mark', 'Brown', 'mark.brown@gmail.com', crypt('Mark', gen_salt('bf')), '2024-04-16 09:00:00'::timestamp, TRUE),
('Emily', 'Johnson', 'emily.johnson@gmail.com', crypt('Emily', gen_salt('bf')), '2024-04-17 10:00:00'::timestamp, TRUE),
('Jon', 'Jones', 'jon.jones@gmail.com', crypt('Jon', gen_salt('bf')), '2024-04-18 10:00:00'::timestamp, TRUE),
('Lucy', 'Wayne', 'lucy.wayne@gmail.com', crypt('Lucy', gen_salt('bf')), '2024-04-19 12:00:00'::timestamp, TRUE);


INSERT INTO AdministrativeStaff (FirstName, LastName, Email, Password, Role)
VALUES 
('Lucas', 'White', 'lucas.white@gmail.com',  crypt('Lucas', gen_salt('bf')), 'General Manager'),
('Kai','Cenat', 'kai.cenat@gmail.com',  crypt('Kai', gen_salt('bf')), 'Receptionist'),
('Duke', 'Dennis', 'duke.dennis@gmail.com', crypt('Duke', gen_salt('bf')), 'Equipment Manager');

INSERT INTO Rooms (RoomName, Capacity)
VALUES
('Yoga Studio', 10),
('Cycling Room', 15),
('Weight Room', 50);

INSERT INTO Equipment (EquipmentName, MaintenanceDate)
VALUES 
('Treadmill #1', '2023-08-01'),
('Treadmill #2', '2023-08-01'),
('Treadmill #3', '2023-08-01'),
('Treadmill #4', '2023-08-01'),
('Rowing Machine #1', '2023-09-12'),
('Dumbbell Set #1', '2023-07-05'),
('Dumbbell Set #2', '2023-07-05'),
('Cable Machine #1', '2023-07-05'),
('Cable Machine #2', '2023-07-05'),
('Bench Set #1', '2023-07-05'),
('Bench Set #2', '2023-07-05');

INSERT INTO PersonalTrainingSessions (MemberID, TrainerID, ScheduledTime, Status)
VALUES 
(2, 4, '2024-04-19 12:00:00'::timestamp, 'Scheduled');

INSERT INTO GroupFitnessClasses (ClassName, DateTime, TrainerID, RoomID)
VALUES 
('Afternoon Yoga', '2024-04-20 12:00:00', 1, 1),
('Evening Cycling', '2024-04-20 18:00:00', 2, 2);

INSERT INTO Billing (MemberID, Amount, Date, PaymentStatus)
VALUES 
(1, 50.00, '2024-04-02', 'Paid'),
(2, 50.00, '2024-04-06', 'Paid');
