USE pathfinder_db;

INSERT INTO Skills (name, category) VALUES
('Python','Programming'),
('C++','Programming'),
('Data Structures','CS Fundamentals'),
('SQL','Databases'),
('Public Speaking','Soft Skills'),
('Machine Learning','AI'),
('Web Development','Web');

INSERT INTO Interests (name) VALUES
('Research'), ('Web Development'), ('Data Science'), ('Teaching');

INSERT INTO Careers (title, description, avg_salary, industry) VALUES
('Software Engineer','Develops software applications and systems.',600000,'IT'),
('Data Scientist','Analyzes data and builds predictive models.',900000,'AI'),
('Database Administrator','Manages and optimizes databases.',700000,'IT'),
('Frontend Developer','Builds user interfaces and web experiences.',550000,'Web');

INSERT INTO CareerSkills (career_id, skill_id, importance) VALUES
(1,1,8), -- SE needs Python
(1,3,9),
(1,4,6),
(2,1,7),
(2,6,9),
(2,4,6),
(3,4,10),
(4,7,9),
(4,1,5);

-- Create example users with placeholder password hashes (use app to register real users)
INSERT INTO Users (first_name, last_name, email, password_hash, highest_education, cgpa) VALUES
('Ankush','Chauhan','ankush@example.com','$2b$12$abcdefghijklmnopqrstuv', 'B.Tech',8.00),
('Priya','Sharma','priya@example.com','$2b$12$abcdefghijklmnopqrstu1', 'B.Sc',7.50);

-- Example UserSkills
INSERT INTO UserSkills (user_id, skill_id, proficiency) VALUES
(1,1,'high'),
(1,3,'high'),
(1,4,'medium'),
(2,4,'high'),
(2,5,'medium');

-- Example UserInterests
INSERT INTO UserInterests (user_id, interest_id) VALUES
(1,2),
(1,3);