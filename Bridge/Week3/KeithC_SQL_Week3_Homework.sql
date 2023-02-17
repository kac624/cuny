-- Creating and populating dimension tables

CREATE TABLE `access`.`users` (
  `userID` INT NOT NULL AUTO_INCREMENT,
  `userName` CHAR(45) NULL,
  PRIMARY KEY (`userID`)
);
  
INSERT INTO users (userName)
VALUES 
	('Modesto'),
    ('Ayine'),
    ('Christopher'),
    ('Cheong woo'),
    ('Saulat'),
    ('Heidy');
  
CREATE TABLE `access`.`groupings` (
  `groupID` INT NOT NULL AUTO_INCREMENT,
  `groupName` CHAR(45) NULL,
  PRIMARY KEY (`groupID`)
);
 
INSERT INTO groupings (groupName)
VALUES 
	('I.T.'),
    ('Sales'),
    ('Administration'),
    ('Operations');
 
CREATE TABLE `access`.`rooms` (
  `roomID` INT NOT NULL AUTO_INCREMENT,
  `roomName` CHAR(45) NULL,
  PRIMARY KEY (`roomID`)
);

INSERT INTO rooms (roomName)
VALUES 
	('101'),
    ('102'),
    ('Auditorium A'),
    ('Auditorium B');
  
-- Creating fact tables with foreign key relationships

CREATE TABLE `access`.`user_group` (
  `userID` INT,
  `groupID` INT,
  FOREIGN KEY (userID) REFERENCES users(userID),
  FOREIGN KEY (groupID) REFERENCES groupings(groupID)
);

CREATE TABLE `access`.`group_room` (
  `groupID` INT,
  `roomID` INT,
  FOREIGN KEY (groupID) REFERENCES groupings(groupID),
  FOREIGN KEY (roomID) REFERENCES rooms(roomID)
);

-- Insert mappings of users to groups and groups to rooms

INSERT INTO user_group (userID, groupID)
VALUES 
	(1,1),
    (2,1),
    (3,2),
    (4,2),
    (5,3);

INSERT INTO group_room (groupID, roomID)
VALUES 
	(1,1),
    (1,2),
    (2,2),
    (2,3);
    
-- Select statments


SELECT groupings.groupID, groupName, userName FROM groupings
LEFT JOIN user_group ON groupings.groupID = user_group.groupID
LEFT JOIN users ON user_group.userID = users.userID;


SELECT rooms.roomID, roomName, groupName FROM rooms
LEFT JOIN group_room ON rooms.roomID = group_room.roomID
LEFT JOIN groupings ON group_room.groupID = groupings.groupID;


SELECT users.userID, userName, groupName, roomName FROM users
LEFT JOIN user_group ON  users.userID = user_group.userID
LEFT JOIN groupings ON user_group.groupID = groupings.groupID
LEFT JOIN group_room ON groupings.groupID = group_room.groupID
LEFT JOIN rooms ON group_room.roomID = rooms.roomID