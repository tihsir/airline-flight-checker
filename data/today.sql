DROP DATABASE flightsdatabase2;
CREATE DATABASE flightsdatabase2;
USE flightsdatabase2;

DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
	userID INT PRIMARY KEY,
	username VARCHAR(100),
	password VARCHAR(100),
	phoneNumber VARCHAR(15)
);

DROP TABLE IF EXISTS Airlines;
CREATE TABLE Airlines (
	IATAcodeAirline VARCHAR(3) PRIMARY KEY,
	airline VARCHAR(100)
);

DROP TABLE IF EXISTS Airports;
CREATE TABLE Airports (
	IATAcodeAirport VARCHAR(3) PRIMARY KEY,
	airport VARCHAR(100),
	city VARCHAR(100),
	state VARCHAR(100)
);

DROP TABLE IF EXISTS Aircrafts;
CREATE TABLE Aircrafts (
	tailNumber VARCHAR(100) PRIMARY KEY,
	company VARCHAR(100),
	aircraftModel VARCHAR(100)
);
/*SET SQL_SAFE_UPDATES = 0;
DELETE FROM Aircrafts WHERE company IS NOT NULL;
SET SQL_SAFE_UPDATES = 1;
SELECT COUNT(*) FROM Aircrafts;*/

DROP TABLE IF EXISTS Flights;
CREATE TABLE Flights (
	flightNumber INT PRIMARY KEY,
	airline VARCHAR(3),
	tailNumber VARCHAR(100),
	year INT,
	month VARCHAR(15),
	day VARCHAR(2),
	dayOfTheWeek VARCHAR(15),
	originAirport VARCHAR(3), 
	destinationAirport VARCHAR(3),
	departureDelay VARCHAR(10),
	cancelled INT,
	FOREIGN KEY (airline) REFERENCES Airlines(IATAcodeAirline),
	FOREIGN KEY (originAirport) REFERENCES Airports(IATAcodeAirport),
	FOREIGN KEY (destinationAirport) REFERENCES Airports(IATAcodeAirport),
	FOREIGN KEY (tailNumber) REFERENCES Aircrafts(tailNumber)
);
/*SET SQL_SAFE_UPDATES = 0;
DELETE FROM Flights WHERE flightNumber IS NOT NULL;
SET SQL_SAFE_UPDATES = 1;
SELECT COUNT(*) FROM Flights;*/

/*DROP DATABASE flightsdatabase2;
CREATE DATABASE flightsdatabase2;
USE flightsdatabase2;
SELECT A.airline, COUNT(F.flightNumber) AS TotalFlights
FROM Airlines A
JOIN Flights F ON A.IATAcodeAirline = F.airline
WHERE F.month = '12'
GROUP BY A.airline
ORDER BY TotalFlights DESC;*/


DROP TABLE IF EXISTS Flights;
CREATE TABLE Flights (
	flightNumber INT PRIMARY KEY,
	airline VARCHAR(3),
	tailNumber VARCHAR(100),
	year INT,
	month VARCHAR(15),
	day VARCHAR(2),
	dayOfTheWeek VARCHAR(15),
	originAirport VARCHAR(3), 
	destinationAirport VARCHAR(3),
	departureDelay INT,
	cancelled INT,
	FOREIGN KEY (airline) REFERENCES Airlines(IATAcodeAirline),
	FOREIGN KEY (originAirport) REFERENCES Airports(IATAcodeAirport),
	FOREIGN KEY (destinationAirport) REFERENCES Airports(IATAcodeAirport),
	FOREIGN KEY (tailNumber) REFERENCES Aircrafts(tailNumber)
);

DROP TABLE IF EXISTS userRating;
CREATE TABLE userRating (
	userID INT, 
	airline VARCHAR(3),
	userRating INT,
	PRIMARY KEY (userID, airline),
	FOREIGN KEY (userID) REFERENCES Users(userID),
	FOREIGN KEY (airline) REFERENCES Airlines(IATAcodeAirline)
);

SELECT COUNT(*) FROM Aircrafts;

SELECT A.IATAcodeAirline, COUNT(F.departureDelay) AS NumDepartureDelay 
FROM Airlines A 
JOIN Flights F ON A.IATAcodeAirline = F.airline 
GROUP BY A.IATAcodeAirline 
ORDER BY NumDepartureDelay DESC;