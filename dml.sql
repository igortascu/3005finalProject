-- Inserting into Members
INSERT INTO Members (FirstName, LastName, Email, DateOfBirth, FitnessGoals, HealthMetrics)
VALUES 
('John', 'Doe', 'john.doe@example.com', '1985-02-15', '{"weightTarget":"180lbs","distanceTarget":"5km"}', '{"currentWeight":"200lbs","heartRate":"75bpm"}'),
('Jane', 'Smith', 'jane.smith@example.com', '1990-07-22', '{"weightTarget":"130lbs","timeTarget":"30mins"}', '{"currentWeight":"150lbs","heartRate":"80bpm"}');

-- Inserting into Trainers
INSERT INTO Trainers (FirstName, LastName, Email, Availability)
VALUES 
('Mark', 'Brown', 'mark.brown@example.com', '["Monday 09:00-11:00", "Wednesday 14:00-16:00"]'),
('Emily', 'Johnson', 'emily.johnson@example.com', '["Tuesday 10:00-12:00", "Thursday 15:00-17:00"]');

-- Inserting into AdministrativeStaff
INSERT INTO AdministrativeStaff (FirstName, LastName, Email, Role)
VALUES 
('Lucas', 'White', 'lucas.white@example.com', 'Manager'),
('Olivia', 'Davis', 'olivia.davis@example.com', 'Receptionist');

-- Inserting into Rooms -- Adjust room names and capacities as needed
INSERT INTO Rooms (RoomName, Capacity)
VALUES 
('Yoga Studio', 20),
('Cycling Room', 15),
('Pilates Room', 10);

-- Inserting into Equipment -- Adjust names and maintenance dates as needed
INSERT INTO Equipment (EquipmentName, MaintenanceDate)
VALUES 
('Treadmill #1', '2023-08-01'),
('Rowing Machine #1', '2023-09-12'),
('Dumbbell Set #1', '2023-07-05');

-- Optionally, you can insert dummy data into PersonalTrainingSessions, GroupFitnessClasses, and Billing if needed for testing
-- For example, inserting into PersonalTrainingSessions
INSERT INTO PersonalTrainingSessions (MemberID, TrainerID, DateTime, Status)
VALUES 
(1, 1, '2024-04-15 09:00:00', 'Scheduled'),
(2, 2, '2024-04-16 10:00:00', 'Scheduled');

-- For example, inserting into GroupFitnessClasses
INSERT INTO GroupFitnessClasses (ClassName, DateTime, TrainerID, RoomID)
VALUES 
('Morning Yoga', '2024-04-20 08:00:00', 1, 1),
('Evening Cycling', '2024-04-20 18:00:00', 2, 2);

-- Inserting into Billing
INSERT INTO Billing (MemberID, Amount, Date, PaymentStatus)
VALUES 
(1, 50.00, '2024-04-01', 'Paid'),
(2, 75.00, '2024-04-01', 'Unpaid');
