-- Q#1 Create Videos table and insert values

CREATE TABLE `videos`.`videos` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Title` CHAR(50) NULL,
  `Length` INT NULL,
  `URL` CHAR(50) NULL,
  PRIMARY KEY (`ID`));

INSERT INTO videos (Title, Length, URL)
VALUES ('MySQL Tutorial for Beginners',190,'youtube.com/watch?v=7S_tz1z_5bA');

INSERT INTO videos (Title, Length, URL)
VALUES ('MySQL - The Basics',17,'youtube.com/watch?v=Cz3WcZLRaWc');

INSERT INTO videos (Title, Length, URL)
VALUES ('MySQL IN 10 MINUTES',11,'youtube.com/watch?v=2bW3HuaAUcY');

INSERT INTO videos (Title, Length, URL)
VALUES ('How to Use MySQL',18,'youtube.com/watch?v=mN2_1NjNWa4');

INSERT INTO videos (Title, Length, URL)
VALUES ('MySQL Workbench Tutorial',14,'youtube.com/watch?v=chezeWdTHbo&t=62s');

-- Q#2 Create Reviews table and insert values

CREATE TABLE `videos`.`reviews` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `User` CHAR(45) NULL,
  `Rating` INT NULL,
  `Review` CHAR(100) NULL,
  `VideoID` CHAR(45) NULL,
  PRIMARY KEY (`ID`));
  
INSERT INTO reviews (User, Rating, Review, VideoID)
VALUES ('SQL_lover555', 5, 'Thank you, this video is great!', 1);

INSERT INTO reviews (User, Rating, Review, VideoID)
VALUES ('Im_confused', 1, 'I dont understand!', 1);

INSERT INTO reviews (User, Rating, Review, VideoID)
VALUES ('Wrong_rater', 2, 'Terrific video!', 2);

INSERT INTO reviews (User, Rating, Review, VideoID)
VALUES ('Middle_guy', 3, 'It was okay.', 3);

INSERT INTO reviews (User, Rating, Review, VideoID)
VALUES ('Almost_there', 5, 'The video was good, but I wanted more detail.', 4);

INSERT INTO reviews (User, Rating, Review, VideoID)
VALUES ('Um_actually', 2, 'He should have given more info on Joins.', 5);

INSERT INTO reviews (User, Rating, Review, VideoID)
VALUES ('Easy_to_pleasey', 5, 'The most amazing video ever.', 5);

-- Q#3 JOIN Statement showing info from both tables

SELECT reviews.ID, User, Rating, Review, VideoID, Title, Length
FROM reviews
INNER JOIN videos ON reviews.VideoID = videos.ID
ORDER BY Rating DESC