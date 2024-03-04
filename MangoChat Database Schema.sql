-- Create database
CREATE DATABASE IF NOT EXISTS mangochat;
USE mangochat;

-- Table for Users
CREATE TABLE IF NOT EXISTS user (
    userID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Table for Channels
CREATE TABLE IF NOT EXISTS channel (
    channelID INT AUTO_INCREMENT PRIMARY KEY,
    channelName VARCHAR(100) NOT NULL
);

-- Table for User-Channel Relationship
CREATE TABLE IF NOT EXISTS user_channel (
    userChanID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,
    channelID INT,
    isModerator BOOLEAN,
    isBanned BOOLEAN,
    FOREIGN KEY (userID) REFERENCES user(userID) ON DELETE CASCADE,
    FOREIGN KEY (channelID) REFERENCES channel(channelID) ON DELETE CASCADE,
    UNIQUE(userID, channelID)
);

-- Table for Messages
CREATE TABLE IF NOT EXISTS message (
    messageID INT AUTO_INCREMENT PRIMARY KEY,
    channelID INT,
    senderID INT,
    content TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channelID) REFERENCES channel(channelID) ON DELETE CASCADE,
    FOREIGN KEY (senderID) REFERENCES user(userID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS friend (
    friendID INT AUTO_INCREMENT PRIMARY KEY,
    userID1 INT,
    userID2 INT,
    status ENUM('Pending', 'Accepted', 'Blocked') NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (userID1) REFERENCES user(userID) ON DELETE CASCADE,
    FOREIGN KEY (userID2) REFERENCES user(userID) ON DELETE CASCADE,
    UNIQUE(userID1, userID2)
);

CREATE TABLE IF NOT EXISTS block (
    blockID INT AUTO_INCREMENT PRIMARY KEY,
    blockerID INT,
    blockedID INT,
    FOREIGN KEY (blockerID) REFERENCES user(userID) ON DELETE CASCADE,
    FOREIGN KEY (blockedID) REFERENCES user(userID) ON DELETE CASCADE,
    UNIQUE(blockerID, blockedID)
);


-- SQL Commands with placeholder values

-- Insert a new channel into Channels table
INSERT INTO channel(channelName) VALUES ('New Channel Name');

-- Delete a channel by its ID
DELETE FROM channel WHERE channelID = 1;

-- Insert a new user into Users table
INSERT INTO user (username, password) VALUES ('NewUser', 'password123');
INSERT INTO user (username, password) VALUES ('anotherUser', 'password124');

-- Adding Friend
-- Assuming both users already exist in Users table
-- User1 sends friend request to User2
INSERT INTO friend (userID1, userID2, status) VALUES (1, 2, 'Pending');

-- User2 accepts the friend request
UPDATE friend SET status = 'Accepted' WHERE userID1 = 1 AND userID2 = 2;

-- Removing Friend
-- Assuming both users are already friends
-- User1 removes User2 from friends
DELETE FROM friend WHERE (userID1 = 1 AND userID2 = 2) OR (userID1 = 2 AND userID2 = 1);

-- Blocking User
-- User1 blocks User2
INSERT INTO block (blockerID, blockedID) VALUES (1, 2);

-- Insert a new message into Messages table
INSERT INTO message (messageID, senderID, content) VALUES (1, 1, 'Hello, this is a message!');


