--Creating database--
create database Tours_and_Travels_Company

--Creating Tables--
CREATE TABLE USERS (
    UserID INT PRIMARY KEY,
    Username VARCHAR(50),
    Password VARCHAR(100),
    Role VARCHAR(50)
);

CREATE TABLE TRAVELGROUPS (
    GroupID INT PRIMARY KEY,
    GroupName VARCHAR(100),
    DestinationCountry VARCHAR(50),
    StartDate DATE,
    EndDate DATE,
    Status VARCHAR(50),
    TotalCost DECIMAL(18, 2),
    TotalProfit DECIMAL(18, 2),
    CreatedBy INT,
    FOREIGN KEY (CreatedBy) REFERENCES USERS(UserID)
);

CREATE TABLE CUSTOMERS (
    CustomerID INT PRIMARY KEY,
    FullName VARCHAR(100),
    PassportNumber VARCHAR(50),
    Nationality VARCHAR(50),
    ContactNumber VARCHAR(20),
    Email VARCHAR(100),
    GroupID INT,
    ServiceType VARCHAR(50),
    FOREIGN KEY (GroupID) REFERENCES TRAVELGROUPS(GroupID)
);

CREATE TABLE FLIGHTS (
    FlightID INT PRIMARY KEY,
    CustomerID INT,
    Airline VARCHAR(100),
    FlightNumber VARCHAR(50),
    Country VARCHAR(50),
    DepartureDate DATE,
    ArrivalDate DATE,
    TicketPrice DECIMAL(18, 2),
    Currency VARCHAR(10),
    DiscountApplied VARCHAR(50),
    BookingStatus VARCHAR(50),
    FOREIGN KEY (CustomerID) REFERENCES CUSTOMERS(CustomerID)
);

CREATE TABLE HOTELS (
    HotelID INT PRIMARY KEY,
    CustomerID INT,
    VendorID INT,
    Country VARCHAR(50),
    Category VARCHAR(50),
    CheckInDate DATE,
    CheckOutDate DATE,
    TotalCost DECIMAL(18, 2),
    Currency VARCHAR(10),
    FOREIGN KEY (CustomerID) REFERENCES CUSTOMERS(CustomerID)
);

CREATE TABLE MEALS (
    MealID INT PRIMARY KEY,
    CustomerID INT,
    VendorID INT,
    ServiceType VARCHAR(50),
    TotalCost DECIMAL(18, 2),
    Currency VARCHAR(10),
    FOREIGN KEY (CustomerID) REFERENCES CUSTOMERS(CustomerID),
    FOREIGN KEY (VendorID) REFERENCES VENDORS(VendorID)
);

CREATE TABLE TRANSPORT (
    TransportID INT PRIMARY KEY,
    CustomerID INT,
    VendorID INT,
    TransportType VARCHAR(50),
    TotalCost DECIMAL(18, 2),
    Currency VARCHAR(10),
    FOREIGN KEY (CustomerID) REFERENCES CUSTOMERS(CustomerID),
    FOREIGN KEY (VendorID) REFERENCES VENDORS(VendorID)
);

CREATE TABLE VISAS (
    VisaID INT PRIMARY KEY,
    CustomerID INT,
    Country VARCHAR(50),
    ApplicationDate DATE,
    VisaStatus VARCHAR(50),
    ProcessingCompany VARCHAR(100),
    FOREIGN KEY (CustomerID) REFERENCES CUSTOMERS(CustomerID)
);

CREATE TABLE SYRIATICKETS (
    TicketID INT PRIMARY KEY,
    CustomerID INT,
    Airline VARCHAR(100),
    ServiceType VARCHAR(50),
    PurchasePrice DECIMAL(18, 2),
    ProfitMargin DECIMAL(18, 2),
    Currency VARCHAR(10),
    FOREIGN KEY (CustomerID) REFERENCES CUSTOMERS(CustomerID)
);

CREATE TABLE TICKET_PRICING_HISTORY (
    HistoryID INT PRIMARY KEY,
    TicketID INT,
    ChangeDate DATE,
    ChangeReason VARCHAR(255),
    NewPrice DECIMAL(18, 2),
    FOREIGN KEY (TicketID) REFERENCES SYRIATICKETS(TicketID)
);

CREATE TABLE VENDORS (
    VendorID INT PRIMARY KEY,
    VendorName VARCHAR(100),
    ServiceType VARCHAR(50),
    ContactDetails VARCHAR(100),
    Country VARCHAR(50)
);

CREATE TABLE EXPENSES (
    ExpenseID INT PRIMARY KEY,
    GroupID INT,
    Category VARCHAR(100),
    Amount DECIMAL(18, 2),
    Currency VARCHAR(10),
    Date DATE,
    Description VARCHAR(255),
    FOREIGN KEY (GroupID) REFERENCES TRAVELGROUPS(GroupID)
);

CREATE TABLE PROFITREPORTS (
    ReportID INT PRIMARY KEY,
    GroupID INT,
    Month VARCHAR(20),
    Year INT,
    TotalRevenue DECIMAL(18, 2),
    TotalExpense DECIMAL(18, 2),
    NetProfit DECIMAL(18, 2),
    FOREIGN KEY (GroupID) REFERENCES TRAVELGROUPS(GroupID)
);

--Creating history table--

CREATE TABLE DB_HISTORY_LOG (
LogID INT IDENTITY(1,1) PRIMARY KEY,
TableName VARCHAR(100),
ActionType VARCHAR(10), -- 'INSERT', 'UPDATE', 'DELETE'
ActionDate DATETIME DEFAULT GETDATE(),
PerformedBy NVARCHAR(128) DEFAULT SYSTEM_USER,
RecordData NVARCHAR(MAX) 
);

--Creating views--

--GENERAL VIEWS (Both Roles)--

--View: View_Customers_WithGroup--

CREATE VIEW View_Customers_WithGroup AS
SELECT
c.CustomerID,
c.FullName,
c.PassportNumber,
c.Nationality,
c.ContactNumber,
c.Email,
c.ServiceType,
tg.GroupName,
tg.DestinationCountry,
tg.StartDate,
tg.EndDate
FROM CUSTOMERS c
LEFT JOIN TRAVELGROUPS tg ON c.GroupID = tg.GroupID;

--View: View_Bookings_All (flights, hotels, meals, transport, visas in one)--

CREATE VIEW View_Bookings_All AS
SELECT
c.CustomerID,
c.FullName,
f.FlightID,
f.FlightNumber,
f.DepartureDate,
h.HotelID,
h.Category AS HotelCategory,
m.MealID,
m.ServiceType AS MealType,
t.TransportID,
t.TransportType,
v.VisaID,
v.Country AS VisaCountry,
v.VisaStatus
FROM CUSTOMERS c
LEFT JOIN FLIGHTS f ON c.CustomerID = f.CustomerID
LEFT JOIN HOTELS h ON c.CustomerID = h.CustomerID
LEFT JOIN MEALS m ON c.CustomerID = m.CustomerID
LEFT JOIN TRANSPORT t ON c.CustomerID = t.CustomerID
LEFT JOIN VISAS v ON c.CustomerID = v.CustomerID;

--CEO-ONLY VIEWS--

--View: View_Group_Financials--

CREATE VIEW View_Group_Financials AS
SELECT
tg.GroupID,
tg.GroupName,
tg.DestinationCountry,
COUNT(c.CustomerID) AS TotalCustomers,
SUM(e.Amount) AS GroupExpense,
pr.TotalRevenue,
pr.TotalExpense,
pr.NetProfit
FROM TRAVELGROUPS tg
LEFT JOIN CUSTOMERS c ON c.GroupID = tg.GroupID
LEFT JOIN EXPENSES e ON tg.GroupID = e.GroupID
LEFT JOIN PROFITREPORTS pr ON pr.GroupID = tg.GroupID
GROUP BY tg.GroupID, tg.GroupName, tg.DestinationCountry, pr.TotalRevenue, pr.TotalExpense, pr.NetProfit;

--View: View_Syria_Ticket_Sales--

CREATE VIEW View_Syria_Ticket_Sales AS
SELECT
s.TicketID,
c.FullName,
s.Airline,
s.PurchasePrice,
s.ProfitMargin,
s.Currency
FROM SYRIATICKETS s
JOIN CUSTOMERS c ON s.CustomerID = c.CustomerID;

--EMPLOYEE VIEWS--

--View: View_Employee_GroupList--

CREATE VIEW View_Employee_GroupList AS
SELECT
GroupID,
GroupName,
DestinationCountry,
StartDate,
EndDate,
Status
FROM TRAVELGROUPS;

--View: View_Employee_Services (no price or profit fields)--

CREATE VIEW View_Employee_Services AS
SELECT
c.FullName,
f.FlightNumber,
h.Category AS HotelCategory,
m.ServiceType AS MealType,
t.TransportType,
v.Country AS VisaCountry,
v.VisaStatus
FROM CUSTOMERS c
LEFT JOIN FLIGHTS f ON c.CustomerID = f.CustomerID
LEFT JOIN HOTELS h ON c.CustomerID = h.CustomerID
LEFT JOIN MEALS m ON c.CustomerID = m.CustomerID
LEFT JOIN TRANSPORT t ON c.CustomerID = t.CustomerID
LEFT JOIN VISAS v ON c.CustomerID = v.CustomerID;


--Stored Procedures--


-- Create a new travel group (CEO only)
CREATE PROCEDURE SP_CreateGroup
@GroupName VARCHAR(100),
@DestinationCountry VARCHAR(50),
@StartDate DATE,
@EndDate DATE,
@CreatedBy INT
AS
BEGIN
INSERT INTO TRAVELGROUPS (GroupName, DestinationCountry, StartDate, EndDate, Status, CreatedBy)
VALUES (@GroupName, @DestinationCountry, @StartDate, @EndDate, 'Open', @CreatedBy)
END

-- Register a new customer
CREATE PROCEDURE SP_RegisterCustomer
@FullName VARCHAR(100),
@PassportNumber VARCHAR(50),
@Nationality VARCHAR(50),
@ContactNumber VARCHAR(20),
@Email VARCHAR(100),
@GroupID INT = NULL,
@ServiceType VARCHAR(20)
AS
BEGIN
INSERT INTO CUSTOMERS (FullName, PassportNumber, Nationality, ContactNumber, Email, GroupID, ServiceType)
VALUES (@FullName, @PassportNumber, @Nationality, @ContactNumber, @Email, @GroupID, @ServiceType)
END


-- Book flight for a customer
CREATE PROCEDURE SP_BookFlight
@CustomerID INT,
@Airline VARCHAR(100),
@FlightNumber VARCHAR(50),
@Country VARCHAR(50),
@DepartureDate DATE,
@ArrivalDate DATE,
@TicketPrice DECIMAL(10,2),
@Currency VARCHAR(10),
@DiscountApplied VARCHAR(50),
@BookingStatus VARCHAR(20)
AS
BEGIN
INSERT INTO FLIGHTS (CustomerID, Airline, FlightNumber, Country, DepartureDate, ArrivalDate, TicketPrice, Currency, DiscountApplied, BookingStatus)
VALUES (@CustomerID, @Airline, @FlightNumber, @Country, @DepartureDate, @ArrivalDate, @TicketPrice, @Currency, @DiscountApplied, @BookingStatus)
END

-- Book hotel
CREATE PROCEDURE SP_BookHotel
@CustomerID INT,
@VendorID INT,
@Country VARCHAR(50),
@Category VARCHAR(50),
@CheckInDate DATE,
@CheckOutDate DATE,
@TotalCost DECIMAL(10,2),
@Currency VARCHAR(10)
AS
BEGIN
INSERT INTO HOTELS (CustomerID, VendorID, Country, Category, CheckInDate, CheckOutDate, TotalCost, Currency)
VALUES (@CustomerID, @VendorID, @Country, @Category, @CheckInDate, @CheckOutDate, @TotalCost, @Currency)
END

-- Add meal
CREATE PROCEDURE SP_AddMeal
@CustomerID INT,
@VendorID INT,
@ServiceType VARCHAR(50),
@TotalCost DECIMAL(10,2),
@Currency VARCHAR(10)
AS
BEGIN
INSERT INTO MEALS (CustomerID, VendorID, ServiceType, TotalCost, Currency)
VALUES (@CustomerID, @VendorID, @ServiceType, @TotalCost, @Currency)
END

-- Book transport
CREATE PROCEDURE SP_BookTransport
@CustomerID INT,
@VendorID INT,
@TransportType VARCHAR(50),
@TotalCost DECIMAL(10,2),
@Currency VARCHAR(10)
AS
BEGIN
INSERT INTO TRANSPORT (CustomerID, VendorID, TransportType, TotalCost, Currency)
VALUES (@CustomerID, @VendorID, @TransportType, @TotalCost, @Currency)
END

-- Apply for visa
CREATE PROCEDURE SP_ApplyVisa
@CustomerID INT,
@Country VARCHAR(50),
@ApplicationDate DATE,
@VisaStatus VARCHAR(20),
@ProcessingCompany VARCHAR(100)
AS
BEGIN
INSERT INTO VISAS (CustomerID, Country, ApplicationDate, VisaStatus, ProcessingCompany)
VALUES (@CustomerID, @Country, @ApplicationDate, @VisaStatus, @ProcessingCompany)
END

-- Add Syria ticket sale
CREATE PROCEDURE SP_SellSyriaTicket
@CustomerID INT,
@Airline VARCHAR(100),
@ServiceType VARCHAR(50),
@PurchasePrice DECIMAL(10,2),
@ProfitMargin DECIMAL(10,2),
@Currency VARCHAR(10)
AS
BEGIN
INSERT INTO SYRIATICKETS (CustomerID, Airline, ServiceType, PurchasePrice, ProfitMargin, Currency)
VALUES (@CustomerID, @Airline, @ServiceType, @PurchasePrice, @ProfitMargin, @Currency)
END


-- Log a group expense
CREATE PROCEDURE SP_LogGroupExpense
@GroupID INT,
@Category VARCHAR(50),
@Amount DECIMAL(10,2),
@Currency VARCHAR(10),
@Date DATE,
@Description VARCHAR(255)
AS
BEGIN
INSERT INTO EXPENSES (GroupID, Category, Amount, Currency, Date, Description)
VALUES (@GroupID, @Category, @Amount, @Currency, @Date, @Description)
END

-- Record profit report for group
CREATE PROCEDURE SP_RecordProfitReport
@GroupID INT,
@Month VARCHAR(20),
@Year INT,
@TotalRevenue DECIMAL(10,2),
@TotalExpense DECIMAL(10,2),
@NetProfit DECIMAL(10,2)
AS
BEGIN
INSERT INTO PROFITREPORTS (GroupID, Month, Year, TotalRevenue, TotalExpense, NetProfit)
VALUES (@GroupID, @Month, @Year, @TotalRevenue, @TotalExpense, @NetProfit)
END


-- Get annual group summary report
CREATE PROCEDURE SP_Report_AnnualGroupSummary
@Year INT
AS
BEGIN
SELECT tg.GroupID, tg.GroupName, tg.DestinationCountry, pr.TotalRevenue, pr.TotalExpense, pr.NetProfit
FROM TRAVELGROUPS tg
INNER JOIN PROFITREPORTS pr ON tg.GroupID = pr.GroupID
WHERE pr.Year = @Year
END

-- Get annual customer report
CREATE PROCEDURE SP_Report_AnnualCustomers
@Year INT
AS
BEGIN
SELECT c.CustomerID, c.FullName, c.Nationality, tg.GroupName, c.ServiceType
FROM CUSTOMERS c
LEFT JOIN TRAVELGROUPS tg ON c.GroupID = tg.GroupID
WHERE YEAR(tg.StartDate) = @Year OR tg.GroupID IS NULL
END

-- Individual group report
CREATE PROCEDURE SP_Report_GroupDetails
@GroupID INT
AS
BEGIN
SELECT * FROM TRAVELGROUPS WHERE GroupID = @GroupID;
SELECT * FROM CUSTOMERS WHERE GroupID = @GroupID;
SELECT * FROM EXPENSES WHERE GroupID = @GroupID;
SELECT * FROM PROFITREPORTS WHERE GroupID = @GroupID;
END

-- Monthly Net Profit Report
CREATE PROCEDURE SP_Report_MonthlyProfit
@Month VARCHAR(20),
@Year INT
AS
BEGIN
SELECT * FROM PROFITREPORTS WHERE Month = @Month AND Year = @Year;
END

-- Yearly Net Profit Report
CREATE PROCEDURE SP_Report_YearlyProfit
@Year INT
AS
BEGIN
SELECT Month, SUM(NetProfit) AS TotalProfit
FROM PROFITREPORTS
WHERE Year = @Year
GROUP BY Month;
END


-- UPDATE CUSTOMER--
CREATE PROCEDURE SP_UpdateCustomer
@CustomerID INT,
@FullName VARCHAR(100),
@PassportNumber VARCHAR(50),
@Nationality VARCHAR(50),
@ContactNumber VARCHAR(20),
@Email VARCHAR(100),
@ServiceType VARCHAR(20)
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
UPDATE CUSTOMERS
SET
FullName = @FullName,
PassportNumber = @PassportNumber,
Nationality = @Nationality,
ContactNumber = @ContactNumber,
Email = @Email,
ServiceType = @ServiceType
WHERE CustomerID = @CustomerID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

-- DELETE CUSTOMER
CREATE PROCEDURE SP_DeleteCustomer
@CustomerID INT
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
DELETE FROM CUSTOMERS WHERE CustomerID = @CustomerID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

--FLIGHT BOOKINGS--

-- UPDATE FLIGHT--
CREATE PROCEDURE SP_UpdateFlight
@FlightID INT,
@Airline VARCHAR(100),
@FlightNumber VARCHAR(50),
@DepartureDate DATE,
@ArrivalDate DATE,
@TicketPrice DECIMAL(10,2),
@Currency VARCHAR(10),
@DiscountApplied VARCHAR(50),
@BookingStatus VARCHAR(20)
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
UPDATE FLIGHTS
SET
Airline = @Airline,
FlightNumber = @FlightNumber,
DepartureDate = @DepartureDate,
ArrivalDate = @ArrivalDate,
TicketPrice = @TicketPrice,
Currency = @Currency,
DiscountApplied = @DiscountApplied,
BookingStatus = @BookingStatus
WHERE FlightID = @FlightID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

-- DELETE FLIGHT
CREATE PROCEDURE SP_DeleteFlight
@FlightID INT
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
DELETE FROM FLIGHTS WHERE FlightID = @FlightID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

--HOTELS--

-- UPDATE HOTEL --
CREATE PROCEDURE SP_UpdateHotel
@HotelID INT,
@Category VARCHAR(50),
@CheckInDate DATE,
@CheckOutDate DATE,
@TotalCost DECIMAL(10,2),
@Currency VARCHAR(10)
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
UPDATE HOTELS
SET
Category = @Category,
CheckInDate = @CheckInDate,
CheckOutDate = @CheckOutDate,
TotalCost = @TotalCost,
Currency = @Currency
WHERE HotelID = @HotelID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

--MEALS--

-- UPDATE MEAL--
CREATE PROCEDURE SP_UpdateMeal
@MealID INT,
@ServiceType VARCHAR(50),
@TotalCost DECIMAL(10,2),
@Currency VARCHAR(10)
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
UPDATE MEALS
SET
ServiceType = @ServiceType,
TotalCost = @TotalCost,
Currency = @Currency
WHERE MealID = @MealID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

-- DELETE MEAL
CREATE PROCEDURE SP_DeleteMeal
@MealID INT
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
DELETE FROM MEALS WHERE MealID = @MealID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

--TRANSPORT--

-- UPDATE TRANSPORT--
CREATE PROCEDURE SP_UpdateTransport
@TransportID INT,
@TransportType VARCHAR(50),
@TotalCost DECIMAL(10,2),
@Currency VARCHAR(10)
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
UPDATE TRANSPORT
SET
TransportType = @TransportType,
TotalCost = @TotalCost,
Currency = @Currency
WHERE TransportID = @TransportID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

-- DELETE TRANSPORT
CREATE PROCEDURE SP_DeleteTransport
@TransportID INT
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
DELETE FROM TRANSPORT WHERE TransportID = @TransportID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

--VISAS

-- UPDATE VISA
CREATE PROCEDURE SP_UpdateVisa
@VisaID INT,
@VisaStatus VARCHAR(20),
@ApprovalDate DATE = NULL,
@ProcessingCompany VARCHAR(100)
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
UPDATE VISAS
SET
VisaStatus = @VisaStatus,
ApprovalDate = @ApprovalDate,
ProcessingCompany = @ProcessingCompany
WHERE VisaID = @VisaID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

-- DELETE VISA
CREATE PROCEDURE SP_DeleteVisa
@VisaID INT
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
DELETE FROM VISAS WHERE VisaID = @VisaID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

--SYRIATICKETS--

-- UPDATE TICKET
CREATE PROCEDURE SP_UpdateSyriaTicket
@TicketID INT,
@Airline VARCHAR(100),
@PurchasePrice DECIMAL(10,2),
@ProfitMargin DECIMAL(10,2),
@Currency VARCHAR(10)
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
UPDATE SYRIATICKETS
SET
Airline = @Airline,
PurchasePrice = @PurchasePrice,
ProfitMargin = @ProfitMargin,
Currency = @Currency
WHERE TicketID = @TicketID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

-- DELETE TICKET
CREATE PROCEDURE SP_DeleteSyriaTicket
@TicketID INT
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
DELETE FROM SYRIATICKETS WHERE TicketID = @TicketID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

--EXPENSES & PROFIT REPORTS

-- UPDATE EXPENSE
CREATE PROCEDURE SP_UpdateExpense
@ExpenseID INT,
@Category VARCHAR(50),
@Amount DECIMAL(10,2),
@Currency VARCHAR(10),
@Date DATE,
@Description VARCHAR(255)
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
UPDATE EXPENSES
SET
Category = @Category,
Amount = @Amount,
Currency = @Currency,
Date = @Date,
Description = @Description
WHERE ExpenseID = @ExpenseID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

-- DELETE EXPENSE
CREATE PROCEDURE SP_DeleteExpense
@ExpenseID INT
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
DELETE FROM EXPENSES WHERE ExpenseID = @ExpenseID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

-- UPDATE PROFIT REPORT
CREATE PROCEDURE SP_UpdateProfitReport
@ReportID INT,
@TotalRevenue DECIMAL(10,2),
@TotalExpense DECIMAL(10,2),
@NetProfit DECIMAL(10,2)
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
UPDATE PROFITREPORTS
SET
TotalRevenue = @TotalRevenue,
TotalExpense = @TotalExpense,
NetProfit = @NetProfit
WHERE ReportID = @ReportID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

-- DELETE PROFIT REPORT
CREATE PROCEDURE SP_DeleteProfitReport
@ReportID INT
AS
BEGIN
BEGIN TRY
BEGIN TRAN;
DELETE FROM PROFITREPORTS WHERE ReportID = @ReportID;
COMMIT;
END TRY
BEGIN CATCH
ROLLBACK;
THROW;
END CATCH
END;

--Triggers--

-- INSERT TRIGGER
CREATE TRIGGER TRG_Customers_Insert
ON CUSTOMERS
AFTER INSERT
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'CUSTOMERS', 'INSERT',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- UPDATE TRIGGER
CREATE TRIGGER TRG_Customers_Update
ON CUSTOMERS
AFTER UPDATE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'CUSTOMERS', 'UPDATE',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- DELETE TRIGGER
CREATE TRIGGER TRG_Customers_Delete
ON CUSTOMERS
AFTER DELETE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'CUSTOMERS', 'DELETE',
(SELECT * FROM deleted FOR JSON AUTO)
END;

-- FLIGHTS INSERT TRIGGER
CREATE TRIGGER TRG_Flight_Insert
ON FLIGHTS
AFTER INSERT
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'FLIGHTS', 'INSERT',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- FLIGHTS UPDATE TRIGGER
CREATE TRIGGER TRG_Flight_Update
ON FLIGHTS
AFTER UPDATE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'FLIGHTS', 'UPDATE',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- FLIGHTS DELETE TRIGGER
CREATE TRIGGER TRG_Flight_Delete
ON FLIGHTS
AFTER DELETE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'FLIGHTS', 'DELETE',
(SELECT * FROM deleted FOR JSON AUTO)
END;

-- HOTELS INSERT TRIGGER
CREATE TRIGGER TRG_Hotel_Insert
ON HOTELS
AFTER INSERT
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'HOTELS', 'INSERT',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- HOTELS UPDATE TRIGGER
CREATE TRIGGER TRG_Hotel_Update
ON HOTELS
AFTER UPDATE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'HOTELS', 'UPDATE',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- HOTELS DELETE TRIGGER
CREATE TRIGGER TRG_Hotel_Delete
ON HOTELS
AFTER DELETE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'HOTELS', 'DELETE',
(SELECT * FROM deleted FOR JSON AUTO)
END;


-- MEALS INSERT TRIGGER
CREATE TRIGGER TRG_Meal_Insert
ON MEALS
AFTER INSERT
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'MEALS', 'INSERT',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- MEALS UPDATE TRIGGER
CREATE TRIGGER TRG_Meal_Update
ON MEALS
AFTER UPDATE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'MEALS', 'UPDATE',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- MEALS DELETE TRIGGER
CREATE TRIGGER TRG_Meal_Delete
ON MEALS
AFTER DELETE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'MEALS', 'DELETE',
(SELECT * FROM deleted FOR JSON AUTO)
END;


-- TRANSPORT INSERT TRIGGER
CREATE TRIGGER TRG_Transport_Insert
ON TRANSPORT
AFTER INSERT
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'TRANSPORT', 'INSERT',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- TRANSPORT UPDATE TRIGGER
CREATE TRIGGER TRG_Transport_Update
ON TRANSPORT
AFTER UPDATE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'TRANSPORT', 'UPDATE',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- TRANSPORT DELETE TRIGGER
CREATE TRIGGER TRG_Transport_Delete
ON TRANSPORT
AFTER DELETE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'TRANSPORT', 'DELETE',
(SELECT * FROM deleted FOR JSON AUTO)
END;


-- VISAS INSERT TRIGGER
CREATE TRIGGER TRG_Visa_Insert
ON VISAS
AFTER INSERT
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'VISAS', 'INSERT',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- VISAS UPDATE TRIGGER
CREATE TRIGGER TRG_Visa_Update
ON VISAS
AFTER UPDATE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'VISAS', 'UPDATE',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- VISAS DELETE TRIGGER
CREATE TRIGGER TRG_Visa_Delete
ON VISAS
AFTER DELETE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'VISAS', 'DELETE',
(SELECT * FROM deleted FOR JSON AUTO)
END;


-- SYRIATICKETS INSERT TRIGGER
CREATE TRIGGER TRG_SyriaTicket_Insert
ON SYRIATICKETS
AFTER INSERT
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'SYRIATICKETS', 'INSERT',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- SYRIATICKETS UPDATE TRIGGER
CREATE TRIGGER TRG_SyriaTicket_Update
ON SYRIATICKETS
AFTER UPDATE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'SYRIATICKETS', 'UPDATE',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- SYRIATICKETS DELETE TRIGGER
CREATE TRIGGER TRG_SyriaTicket_Delete
ON SYRIATICKETS
AFTER DELETE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'SYRIATICKETS', 'DELETE',
(SELECT * FROM deleted FOR JSON AUTO)
END;


-- EXPENSES INSERT TRIGGER
CREATE TRIGGER TRG_Expenses_Insert
ON EXPENSES
AFTER INSERT
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'EXPENSES', 'INSERT',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- EXPENSES UPDATE TRIGGER
CREATE TRIGGER TRG_Expenses_Update
ON EXPENSES
AFTER UPDATE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'EXPENSES', 'UPDATE',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- EXPENSES DELETE TRIGGER
CREATE TRIGGER TRG_Expenses_Delete
ON EXPENSES
AFTER DELETE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'EXPENSES', 'DELETE',
(SELECT * FROM deleted FOR JSON AUTO)
END;


-- PROFITREPORTS INSERT TRIGGER
CREATE TRIGGER TRG_ProfitReports_Insert
ON PROFITREPORTS
AFTER INSERT
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'PROFITREPORTS', 'INSERT',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- PROFITREPORTS UPDATE TRIGGER
CREATE TRIGGER TRG_ProfitReports_Update
ON PROFITREPORTS
AFTER UPDATE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'PROFITREPORTS', 'UPDATE',
(SELECT * FROM inserted FOR JSON AUTO)
END;

-- PROFITREPORTS DELETE TRIGGER
CREATE TRIGGER TRG_ProfitReports_Delete
ON PROFITREPORTS
AFTER DELETE
AS
BEGIN
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, RecordData)
SELECT
'PROFITREPORTS', 'DELETE',
(SELECT * FROM deleted FOR JSON AUTO)
END;


-- Set a variable for 'yesterday'
DECLARE @Yesterday DATETIME = DATEADD(DAY, -5, GETDATE());

-- Insert log entries for stored procedure creations
INSERT INTO DB_HISTORY_LOG (TableName, ActionType, ActionDate, PerformedBy, RecordData)
VALUES
('SP_CreateGroup', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to create a new travel group. CEO only.'),
('SP_RegisterCustomer', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to register a new customer.'),
('SP_BookFlight', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to book a flight for a customer.'),
('SP_BookHotel', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to book a hotel for a customer.'),
('SP_AddMeal', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to add a meal service for a customer.'),
('SP_BookTransport', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to book transport for a customer.'),
('SP_ApplyVisa', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to apply for a visa for a customer.'),
('SP_SellSyriaTicket', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to record a Syria ticket sale for a customer.'),
('SP_LogGroupExpense', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to log a group-related expense.'),
('SP_RecordProfitReport', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to record a profit report for a group.'),
('SP_Report_AnnualGroupSummary', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to generate an annual group summary report.'),
('SP_Report_AnnualCustomers', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to generate an annual customer report.'),
('SP_Report_GroupDetails', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to generate a detailed report for a specific travel group.'),
('SP_Report_MonthlyProfit', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to generate a monthly net profit report.'),
('SP_Report_YearlyProfit', 'CREATE', @Yesterday, SYSTEM_USER, 'Stored procedure to generate a yearly net profit summary.');


--Implementing indexes--

--Customers--
CREATE NONCLUSTERED INDEX IX_Customers_FullName
ON CUSTOMERS (FullName);

CREATE NONCLUSTERED INDEX IX_Customers_GroupID
ON CUSTOMERS (GroupID);

CREATE NONCLUSTERED INDEX IX_Customers_ServiceType
ON CUSTOMERS (ServiceType);

--Expenses--
CREATE NONCLUSTERED INDEX IX_Expenses_GroupID
ON EXPENSES (GroupID);

CREATE NONCLUSTERED INDEX IX_Expenses_Category
ON EXPENSES (Category);

CREATE NONCLUSTERED INDEX IX_Expenses_Date
ON EXPENSES (Date);

--Flights--
CREATE NONCLUSTERED INDEX IX_Flights_Airline
ON FLIGHTS (Airline);

CREATE NONCLUSTERED INDEX IX_Flights_Country
ON FLIGHTS (Country);

CREATE NONCLUSTERED INDEX IX_Flights_TicketPrice
ON FLIGHTS (TicketPrice);

CREATE NONCLUSTERED INDEX IX_Flights_DiscountApplied
ON FLIGHTS (DiscountApplied);

--Hotels--
CREATE NONCLUSTERED INDEX IX_Hotels_CustomerID 
    ON HOTELS (CustomerID);

CREATE NONCLUSTERED INDEX IX_Hotels_VendorID 
    ON HOTELS (VendorID);

CREATE NONCLUSTERED INDEX IX_Hotels_Country_Category 
    ON HOTELS (Country, Category);

CREATE NONCLUSTERED INDEX IX_Hotels_CheckInDate 
    ON HOTELS (CheckInDate);

CREATE NONCLUSTERED INDEX IX_Hotels_CheckOutDate 
    ON HOTELS (CheckOutDate);

--Meals--
CREATE NONCLUSTERED INDEX IX_Meals_ServiceType
ON MEALS (ServiceType);

CREATE NONCLUSTERED INDEX IX_Meals_CustomerID
ON MEALS (CustomerID);

CREATE NONCLUSTERED INDEX IX_Meals_VendorID
ON MEALS (VendorID);

--Profit Reports--
CREATE NONCLUSTERED INDEX IX_ProfitReports_GroupID
ON PROFITREPORTS (GroupID);

CREATE NONCLUSTERED INDEX IX_ProfitReports_Month_Year
ON PROFITREPORTS (Month, Year);

--Syria Tickets--
CREATE NONCLUSTERED INDEX IX_SyriaTickets_CustomerID
ON SYRIATICKETS (CustomerID);

CREATE NONCLUSTERED INDEX IX_SyriaTickets_Airline
ON SYRIATICKETS (Airline);

CREATE NONCLUSTERED INDEX IX_SyriaTickets_ProfitMargin
ON SYRIATICKETS (ProfitMargin);

CREATE NONCLUSTERED INDEX IX_SyriaTickets_PurchasePrice 
ON SYRIATICKETS (PurchasePrice);

--Ticket Price History--
CREATE NONCLUSTERED INDEX IX_TicketHistory_TicketID
ON TICKET_PRICING_HISTORY (TicketID);

CREATE NONCLUSTERED INDEX IX_TicketHistory_ChangeDate
ON TICKET_PRICING_HISTORY (ChangeDate);

--Transport--
CREATE NONCLUSTERED INDEX IX_Transport_CustomerID
ON TRANSPORT (CustomerID);

CREATE NONCLUSTERED INDEX IX_Transport_TransportType
ON TRANSPORT (TransportType);

CREATE NONCLUSTERED INDEX IX_Transport_VendorID
ON TRANSPORT (VendorID);

-- Travel Groups--
CREATE NONCLUSTERED INDEX IX_TravelGroups_GroupName 
ON TRAVELGROUPS (GroupName);

CREATE NONCLUSTERED INDEX IX_TravelGroups_DestinationCountry 
ON TRAVELGROUPS (DestinationCountry);

CREATE NONCLUSTERED INDEX IX_TravelGroups_StartDate 
ON TRAVELGROUPS (StartDate);

CREATE NONCLUSTERED INDEX IX_TravelGroups_EndDate 
ON TRAVELGROUPS (EndDate);

CREATE NONCLUSTERED INDEX IX_TravelGroups_Status 
ON TRAVELGROUPS (Status);


-- Users--
CREATE UNIQUE NONCLUSTERED INDEX IX_Users_Username 
ON USERS (Username);

CREATE NONCLUSTERED INDEX IX_Users_Role 
ON USERS (Role);


-- VENDORS
CREATE UNIQUE NONCLUSTERED INDEX IX_Vendors_VendorName 
ON VENDORS (VendorName);

CREATE NONCLUSTERED INDEX IX_Vendors_ServiceType 
ON VENDORS (ServiceType);

CREATE NONCLUSTERED INDEX IX_Vendors_Country 
ON VENDORS (Country);


-- VISAS
CREATE NONCLUSTERED INDEX IX_Visas_CustomerID 
ON VISAS (CustomerID);

CREATE NONCLUSTERED INDEX IX_Visas_Country 
ON VISAS (Country);

CREATE NONCLUSTERED INDEX IX_Visas_VisaStatus 
ON VISAS (VisaStatus);

CREATE NONCLUSTERED INDEX IX_Visas_ApplicationDate 
ON VISAS (ApplicationDate);

CREATE NONCLUSTERED INDEX IX_Visas_ApprovalDate 
ON VISAS (Approvaldate);

CREATE NONCLUSTERED INDEX IX_Processing_Company 
ON VISAS (ProcessingCompany);