CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Rooms Table
CREATE TABLE Rooms (
    RoomID SERIAL PRIMARY KEY,
    RoomName VARCHAR(255) NOT NULL,
    Capacity INT NOT NULL
);

-- Equipment Table
CREATE TABLE Equipment (
    EquipmentID SERIAL PRIMARY KEY,
    EquipmentName VARCHAR(255) NOT NULL,
    LastMaintenanceDate DATE NOT NULL
);

-- Members Table
CREATE TABLE Members (
    MemberID SERIAL PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    DateOfBirth DATE NOT NULL,
    FitnessGoals TEXT,
    HealthMetrics TEXT 
);

-- Trainers Table
CREATE TABLE Trainers (
    TrainerID SERIAL PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Availability TIMESTAMP NOT NULL,
    IsAvailable BOOLEAN DEFAULT TRUE
);

-- AdministrativeStaff Table
CREATE TABLE AdministrativeStaff (
    StaffID SERIAL PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role VARCHAR(255) NOT NULL
);

-- PersonalTrainingSessions Table
CREATE TABLE PersonalTrainingSessions (
    SessionID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    TrainerID INT REFERENCES Trainers(TrainerID),
    ScheduledTime TIMESTAMP NOT NULL,
    Status VARCHAR(50) DEFAULT 'Free',
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID)
);

-- GroupFitnessClasses Table
CREATE TABLE GroupFitnessClasses (
    ClassID SERIAL PRIMARY KEY,
    ClassName VARCHAR(255) NOT NULL,
    DateTime TIMESTAMP NOT NULL,
    TrainerID INT NOT NULL,
    RoomID INT NOT NULL,
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);

-- Billing Table
CREATE TABLE Billing (
    BillID SERIAL PRIMARY KEY,
    MemberID INT NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    Date DATE NOT NULL,
    PaymentStatus VARCHAR(50) NOT NULL,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

-- MembersGroupClasses Table
CREATE TABLE MembersGroupClasses (
    MemberID INT,
    ClassID INT,
    RegistrationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (MemberID, ClassID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (ClassID) REFERENCES GroupFitnessClasses(ClassID)
);
