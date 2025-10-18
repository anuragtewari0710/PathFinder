DROP DATABASE IF EXISTS pathfinder_db;
CREATE DATABASE pathfinder_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pathfinder_db;

CREATE TABLE Users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100),
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  dob DATE,
  highest_education VARCHAR(100),
  cgpa DECIMAL(4,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Skills (
  skill_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL UNIQUE,
  category VARCHAR(100)
);

CREATE TABLE UserSkills (
  user_skill_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  skill_id INT NOT NULL,
  proficiency ENUM('low','medium','high') DEFAULT 'medium',
  FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (skill_id) REFERENCES Skills(skill_id) ON DELETE CASCADE
);

CREATE TABLE Careers (
  career_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  avg_salary INT,
  industry VARCHAR(100)
);

CREATE TABLE CareerSkills (
  career_skill_id INT AUTO_INCREMENT PRIMARY KEY,
  career_id INT NOT NULL,
  skill_id INT NOT NULL,
  importance INT DEFAULT 5,
  FOREIGN KEY (career_id) REFERENCES Careers(career_id) ON DELETE CASCADE,
  FOREIGN KEY (skill_id) REFERENCES Skills(skill_id) ON DELETE CASCADE
);

CREATE TABLE Interests (
  interest_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE UserInterests (
  user_interest_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  interest_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (interest_id) REFERENCES Interests(interest_id) ON DELETE CASCADE
);

CREATE TABLE Recommendations (
  rec_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  career_id INT NOT NULL,
  score FLOAT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (career_id) REFERENCES Careers(career_id) ON DELETE CASCADE
);
