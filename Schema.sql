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
RecordData NVARCHAR(MAX) -- Will store the changed row(s) as JSON or text
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
