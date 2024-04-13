-- Inserting into Members
INSERT INTO Members (FirstName, LastName, Email, DateOfBirth, FitnessGoals, HealthMetrics)
VALUES 
('Igor', 'Tascu', 'igortascu@gmail.com', '2002-09-10', '{"weightTarget":"180lbs","timeTarget":"3mo"}', '{"currentWeight":"155lbs","heartRate":"50bpm"}'),
('Jane', 'Smith', 'jane.smith@gmail.com', '1990-07-22', '{"weightTarget":"130lbs"}', '{"currentWeight":"150lbs","heartRate":"80bpm"}');

INSERT INTO Trainers (FirstName, LastName, Email, Availability)
VALUES 
('Mark', 'Brown', 'mark.brown@gmail.com', '["Monday 09:00-11:00", "Friday 14:00-16:00"]'),
('Emily', 'Johnson', 'emily.johnson@gmail.com', '["Tuesday 10:00-12:00", "Thursday 15:00-17:00"]');
('Jon', 'Jones', 'jon.jones@gmail.com', '["Saturday 10:00-12:00", "Sunday 15:00-17:00"]');

INSERT INTO AdministrativeStaff (FirstName, LastName, Email, Role)
VALUES 
('Lucas', 'White', 'lucas.white@gmail.com', 'General Manager'),
('Kai','Cenat', 'kai.cenat@gmail.com', 'Receptionist');
('Duke', 'Dennis', 'duke.dennis@gmail.com', 'Equipment Manager');

INSERT INTO Rooms (RoomName, Capacity)
VALUES 
('Yoga Studio', 10),
('Cycling Room', 15),
('Weight Room', 50);

INSERT INTO Equipment (EquipmentName, LastMaintenanceDate)
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
('Bench Set #1', '2023-07-05');
('Bench Set #2', '2023-07-05');

INSERT INTO PersonalTrainingSessions (MemberID, TrainerID, DateTime, Status)
VALUES 
(1, 1, '2024-04-15 09:00:00', 'Scheduled');

INSERT INTO GroupFitnessClasses (ClassName, DateTime, TrainerID, RoomID)
VALUES 
('Morning Yoga', '2024-04-20 08:00:00', 1, 1),
('Evening Cycling', '2024-04-20 18:00:00', 2, 2);

INSERT INTO Billing (MemberID, Amount, Date, PaymentStatus)
VALUES 
(1, 50.00, '2024-04-02', 'Paid');
(2, 50.00, '2024-04-06', 'Paid');
