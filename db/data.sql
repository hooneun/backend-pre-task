-- Contact test data
INSERT INTO contracts_contact (profile_url, name, email, phone, company, position, website, address, birthday, memo, created_at, updated_at) VALUES
('photos/john_doe.jpg', 'John Doe', 'john.doe@email.com', '010-1234-5678', 'Naver', 'Backend Developer', 'https://linkedin.com/in/johndoe', 'Seoul Gangnam-gu Yeoksam-dong 123', '1990-03-15', 'Django expert developer', '2024-01-15 09:00:00', '2024-01-15 09:00:00'),
('photos/jane_smith.jpg', 'Jane Smith', 'jane.smith@email.com', '010-2345-6789', 'Kakao', 'Frontend Developer', 'https://github.com/janesmith', 'Seoul Seocho-gu Seocho-dong 456', '1992-07-22', 'React specialist', '2024-01-15 10:00:00', '2024-01-15 10:00:00'),
('photos/mike_johnson.jpg', 'Mike Johnson', 'mike.johnson@email.com', '010-3456-7890', 'Line', 'DevOps Engineer', 'https://portfolio.mike.com', 'Seoul Jung-gu Myeong-dong 789', '1988-12-03', 'AWS cloud expert', '2024-01-15 11:00:00', '2024-01-15 11:00:00'),
('photos/sarah_wilson.jpg', 'Sarah Wilson', 'sarah.wilson@email.com', '010-4567-8901', 'Woowa Brothers', 'Full Stack Developer', 'https://blog.sarah.dev', 'Seoul Mapo-gu Hongik Univ 321', '1991-05-18', 'Node.js and Python expert', '2024-01-15 12:00:00', '2024-01-15 12:00:00'),
('photos/david_brown.jpg', 'David Brown', 'david.brown@email.com', '010-5678-9012', 'Toss', 'iOS Developer', 'https://apps.apple.com/david', 'Seoul Songpa-gu Jamsil-dong 654', '1989-09-10', 'Swift UI expert', '2024-01-15 13:00:00', '2024-01-15 13:00:00'),
('photos/emma_davis.jpg', 'Emma Davis', 'emma.davis@email.com', '010-6789-0123', 'Coupang', 'Android Developer', 'https://play.google.com/emma', 'Seoul Yeongdeungpo-gu Yeouido 987', '1993-11-25', 'Kotlin and Java expert', '2024-01-15 14:00:00', '2024-01-15 14:00:00'),
('photos/alex_miller.jpg', 'Alex Miller', 'alex.miller@email.com', '010-7890-1234', 'Samsung Electronics', 'AI Developer', 'https://research.samsung.com/alex', 'Suwon Yeongtong-gu Maetan-dong 135', '1987-02-14', 'Machine learning and deep learning research', '2024-01-15 15:00:00', '2024-01-15 15:00:00'),
('photos/lisa_garcia.jpg', 'Lisa Garcia', 'lisa.garcia@email.com', '010-8901-2345', 'NCSOFT', 'Game Developer', 'https://plaync.com/lisa', 'Seongnam Bundang-gu Jeongja-dong 246', '1990-08-07', 'Unity 3D expert', '2024-01-15 16:00:00', '2024-01-15 16:00:00'),
('photos/ryan_thomas.jpg', 'Ryan Thomas', 'ryan.thomas@email.com', '010-9012-3456', 'Spoqa', 'Backend Developer', 'https://spoqa.com/ryan', 'Seoul Gangseo-gu Hwagok-dong 369', '1992-01-30', 'Python Django expert', '2024-01-15 17:00:00', '2024-01-15 17:00:00'),
( 'photos/anna_martinez.jpg', 'Anna Martinez', 'anna.martinez@email.com', '010-0123-4567', 'Daangn Market', 'Data Scientist', 'https://kaggle.com/anna', 'Seoul Yongsan-gu Itaewon-dong 159', '1994-04-12', 'Big data analysis and visualization expert', '2024-01-15 18:00:00', '2024-01-15 18:00:00');

-- Label test data
INSERT INTO contract_label (name, color, created_at, updated_at) VALUES
('Colleague', '#FF5722', '2024-01-15 09:00:00', '2024-01-15 09:00:00'),
('Friend', '#4CAF50', '2024-01-15 09:00:00', '2024-01-15 09:00:00'),
('Family', '#2196F3', '2024-01-15 09:00:00', '2024-01-15 09:00:00'),
('VIP', '#FF9800', '2024-01-15 09:00:00', '2024-01-15 09:00:00'),
('Developer', '#9C27B0', '2024-01-15 09:00:00', '2024-01-15 09:00:00'),
('Designer', '#E91E63', '2024-01-15 09:00:00', '2024-01-15 09:00:00'),
('PM', '#795548', '2024-01-15 09:00:00', '2024-01-15 09:00:00'),
('External', '#607D8B', '2024-01-15 09:00:00', '2024-01-15 09:00:00');

-- Contact-Label relationship test data
INSERT INTO contracts_contact_labels (contact_id, label_id) VALUES
(1, 1), (1, 5),  -- John Doe: Colleague, Developer
(2, 1), (2, 5),  -- Jane Smith: Colleague, Developer
(3, 1), (3, 5),  -- Mike Johnson: Colleague, Developer
(4, 1), (4, 5),  -- Sarah Wilson: Colleague, Developer
(5, 1), (5, 5), -- David Brown: Colleague, Developer
(6, 1), (6, 5), -- Emma Davis: Colleague, Developer
(7, 1), (7, 5), (7, 4), -- Alex Miller: Colleague, Developer, VIP
(8, 2), (8, 5), -- Lisa Garcia: Friend, Developer
(9, 2), (9, 5), -- Ryan Thomas: Friend, Developer
(10, 2), (10, 5); -- Anna Martinez: Friend, Developer