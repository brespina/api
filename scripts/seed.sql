-- ACADEMIC TERMS
INSERT INTO academic_terms (semester, start_date, end_date) VALUES
('Fall 2023', '2023-08-30', '2023-12-05'),
('Fall 2025', '2025-08-28', '2025-12-06');

-- COORDINATORS
INSERT INTO coordinators (user_id, game_id, start_date, end_date) VALUES
(3, 3, '2024-02-01', NULL);

-- EVENT ATTENDEES
INSERT INTO event_attendees (event_id, user_id) VALUES
(1, 1), (1, 2), (2, 2), (2, 3);

-- EVENTS
INSERT INTO events (title, description, location, date_time, end_time, attendance, created_by_officer_id) VALUES
('Fall Kickoff', 'Welcome to the Fall semester!', 'Student Center', '2024-09-01 17:00:00', '2024-09-01 19:00:00', 50, 1),
('Valorant Tournament', '1v1 Valorant Bracket', 'Esports Arena', '2024-11-15 15:00:00', '2024-11-15 20:00:00', 32, 2);

-- GAMES
INSERT INTO games (game_name, bg_image) VALUES
('Overwatch', NULL), ('Valorant', NULL), ('Rocket League', NULL);

-- MATCHES
INSERT INTO matches (team_id, opponent_id, game_id, date_time, watch_link, result) VALUES
(1, 1, 1, '2024-10-01 19:00:00', 'https://twitch.tv/uh-overwatch', 'win'),
(2, 2, 2, '2024-10-10 18:00:00', 'https://twitch.tv/uh-valorant', 'lose');

-- MEDIA
INSERT INTO media (media_image, academic_term_id, uploaded_by_officer_id, date_uploaded) VALUES
(NULL, 1, 1, '2025-02-11'),
(NULL, 2, 2, '2025-06-11');

-- MEMBERSHIPS
INSERT INTO memberships (user_id, start_date, end_date, shirt_size_id) VALUES
(1, '2024-01-12', '2024-12-31', 1), -- Alice, S
(2, '2024-01-17', '2024-12-31', 2), -- Bob, M
(3, '2024-02-01', '2024-12-31', 3); -- Carla, L

-- OFFICERS
INSERT INTO officers (user_id, role_id, start_date, end_date, officer_image) VALUES
(1, 1, '2024-01-11', NULL, NULL),  -- Alice, President
(2, 2, '2024-01-16', NULL, NULL);  -- Bob, VP

-- OPPONENTS
INSERT INTO opponents (opponent_name, game_id, school, logo) VALUES
('Texas A&M', 1, 'Texas A&M University', NULL),
('Baylor Bears', 2, 'Baylor University', NULL),
('UT Longhorns', 2, 'University of Texas', NULL);

-- ROLES
INSERT INTO roles (role_name) VALUES
('President'), ('Vice President'), ('Treasurer'), ('Secretary');

-- SHIRT SIZES
INSERT INTO shirt_sizes (size_name) VALUES
('S'), ('M'), ('L'), ('XL');

-- SPONSORS
INSERT INTO sponsors (end_date, start_date, sponsor_name, sponsor_logo, sponsor_website) VALUES
('2025-12-31', '2024-01-01', 'AMD', NULL, 'https://www.amd.com'),
('2025-06-30', '2024-05-01', 'Corsair', NULL, 'https://www.corsair.com');

-- TEAM MEMBERSHIPS
INSERT INTO team_memberships (team_id, membership_id, player_image, start_date, end_date) VALUES
(1, 1, NULL, '2024-01-12', '2024-12-31'), -- Alice in Overwatch
(2, 2, NULL, '2024-01-17', '2024-12-31'); -- Bob in Valorant

-- TEAMS
INSERT INTO teams (team_name, game_id, coordinator_id, achievements, wins, losses) VALUES
('UH Overwatch', 1, 1, NULL, 0, 0),
('UH Valorant', 2, 2, NULL, 0, 0);

-- USERS
INSERT INTO users (email, password_hash, first_name, last_name, signup_date) VALUES
('alice@uh.edu', '$2b$12$X7sFjR1A6KZZbD3VycKvPeGdFpbpN25Z9zT7.e2cSdnvnlY9vXqye', 'Alice', 'Nguyen', '2024-01-10'),
('bob@uh.edu',  '$2b$12$JsdF1jw9LdsFad9Ssdn234GFYHnsd.9ajF2j.sdfnGnNlsn19jasd9',   'Bob',   'Lee',    '2024-01-15'),
('carla@uh.edu', '$2b$12$Qw8Fj23n0jhqwFh1oKD6as8as98aDHQk18d8JADalKd8jasdks1JQ.', 'Carla', 'Smith',  '2024-01-20');

