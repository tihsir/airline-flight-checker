-- DROP DATABASE flightsdatabase2;
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
	airport VARCHAR(200),
	city VARCHAR(100),
	state VARCHAR(100),
	country VARCHAR(100)
);

DROP TABLE IF EXISTS Aircrafts;
CREATE TABLE Aircrafts (
tailNumber VARCHAR(100) PRIMARY KEY,
company VARCHAR(100),
aircraftModel VARCHAR(100)
);

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

DROP TABLE IF EXISTS userRating;
CREATE TABLE userRating (
userID INT, 
airline VARCHAR(3),
userRating INT,
PRIMARY KEY (userID, airline),
FOREIGN KEY (userID) REFERENCES Users(userID),
FOREIGN KEY (airline) REFERENCES Airlines(IATAcodeAirline)
);

-- SELECT COUNT(*) FROM Aircrafts;
-- SELECT COUNT(*) FROM Airlines;
-- SELECT COUNT(*) FROM Flights;
-- SELECT COUNT(*) FROM userRating;
-- SELECT COUNT(*) FROM Users;
-- SELECT COUNT(*) FROM Airports;

-- SELECT * FROM userRating WHERE userID = 3601;

CREATE DELIMITER //
CREATE PROCEDURE Proced ()
BEGIN
 -- define local vars -- 
  DECLARE varIATA VARCHAR(3);
  DECLARE varAirportName VARCHAR(225);
  DECLARE varAvgDepartureDelay REAL;
  -- declare vars to define --
  DECLARE varBestDestination VARCHAR(100);
  DECLARE varDelayRating VARCHAR(100);
  DECLARE exit_loop BOOLEAN DEFAULT FALSE;
  DECLARE airLineCode VARCHAR(100);
  DECLARE airline VARCHAR(100);
  DECLARE avgAirlineDepartureDelay FLOAT;
	
  -- define and setup cursor --
  DECLARE curr CURSOR FOR (
    SELECT F.originAirport, Ar.airport, AVG(CAST(F.departureDelay AS UNSIGNED)) AS avgDepartureDelay
    FROM Airlines A JOIN Flights F ON A.IATAcodeAirline = F.airline JOIN Airports Ar ON Ar.IATACodeAirport = F.originAirport
    WHERE F.cancelled LIKE 0
    GROUP BY F.originAirport, Ar.airport
  );
  
  -- declare cursor handler to figure out when cursor finishes --
  -- NOT FOUND is an event that is flagged when we are done reading records --
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE; 

  DROP TABLE IF EXISTS TmpTable;
  CREATE Table TmpTable(
    AirportIATA VARCHAR(3) Primary Key,
    AirportName VARCHAR(225),
    DelayRating VARCHAR(225),
    avgAirlineDepartureDelay FLOAT
  );

  -- second adv query -- 
  -- finds the most reliable destination airport from user's chosen origin airport -- 
  SELECT F.originAirport, F.airline, AVG(CAST(F.departureDelay AS UNSIGNED))
  INTO airLineCode, airline, avgAirlineDepartureDelay
  FROM Airlines A JOIN Flights F ON A.IATAcodeAirline = F.airline JOIN Airports Ar ON Ar.IATACodeAirport = F.originAirport
  WHERE F.cancelled LIKE 0
  GROUP BY F.originAirport, F.airline
  ORDER BY avgAirlineDepartureDelay
  LIMIT 1;

  -- create loop structure to iterate through records -- 
  OPEN curr;
	  cloop: loop
	  FETCH curr INTO varIATA, varAirportName, varAvgDepartureDelay;
	  IF exit_loop THEN
		LEAVE cloop;
	  END IF;

	  -- set status -- 
	  IF varAvgDepartureDelay > 60 THEN
		SET varDelayRating = "Least Reliable";
	  ELSEIF varAvgDepartureDelay > 30 THEN
		SET varDelayRating = "Relatively Reliable";
	  ELSEIF varAvgDepartureDelay > 10 THEN
		SET varDelayRating = "Reliable";
	  ELSE
		SET varDelayRating = "Most Reliable";
	  END IF;

	  INSERT INTO TmpTable VALUES (varIATA, varAirportName, varDelayRating, avgAirlineDepartureDelay);

  END LOOP cloop;

  -- free memory -- 
  CLOSE curr; 

  -- obtain desired output -- 
  -- should return IATA, airport name, delay rating, best destination airport --
  SELECT * FROM TmpTable;
  
END //
DELIMITER ; 
CALL Proced();

-- CREATE DELIMITER //
-- CREATE TRIGGER `Users_BEFORE_INSERT` BEFORE INSERT ON `Users` FOR EACH ROW BEGIN
-- 		SET @username = (SELECT username FROM Users WHERE username = new.username);
--         IF @username IS NOT NULL THEN
--             SET @password = (SELECT password FROM Users WHERE username = new.username);
--             IF @password != new.password THEN
--                 SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "Password Is Incorrect. Please Try Again";
--             END IF;
--             IF @password = new.password THEN 
--                 SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "You Are Successfully Logged In";
--             END IF;
--         END IF;
-- END //
-- DELIMITER ;

DROP TRIGGER IF EXISTS Users_BEFORE_INSERT;
DROP TRIGGER IF EXISTS check_username_before_insert;
DELIMITER //
CREATE TRIGGER check_username_before_insert
BEFORE INSERT ON Users
FOR EACH ROW
BEGIN
    DECLARE username_count INT;
    SELECT COUNT(*) INTO username_count FROM Users WHERE username = NEW.username;
    IF username_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username already exists';
    END IF;
END; //
DELIMITER ;
