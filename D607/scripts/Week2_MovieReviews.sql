CREATE SCHEMA `movie_ratings` ;

CREATE TABLE `movie_ratings`.`ratings` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `ReviewerName` CHAR(50) NULL,
  `Whale` INT NULL,
  `Everything` INT NULL,
  `TopGun` INT NULL,
  `Elvis` INT NULL,
  `Avatar` INT NULL,
  PRIMARY KEY (`ID`)
);

INSERT INTO ratings (ReviewerName, Whale, Everything, TopGun, Elvis, Avatar)
VALUES
	('LoriC',5,4,2,2,1),
	('VincentC',NULL,3,4,4,5),
	('RachelJ',2,4,2,5,4),
	('AndrewA',5,4,NULL,NULL,3),
	('ChristianE',3,3,5,2,1);