-- SQLite
--CREATE TABLE info (
--	id INTEGER PRIMARY KEY AUTOINCREMENT,
--    username VARCHAR(255) NOT NULL UNIQUE,
 --   password VARCHAR(255) NOT NULL,
--    phonenumber VARCHAR(255) NOT NULL UNIQUE,
--	email VARCHAR(255) NOT NULL UNIQUE
--);

--INSERT INTO info VALUES (1, 'Ryan', 'JohnnyBoy234', '7605856776', 'mochi456@csu.fullerton.edu');


--CREATE TABLE reviews (

--id INTEGER,
--images BLOB NOT NULL,
--reveiws TEXT NOT NULL,
--FOREIGN KEY(id) REFERENCES info(id)
--);

--ALTER TABLE reviews
--ADD title VARCHAR(255);

--ALTER TABLE reviews
--DROP COLUMN images;

--CREATE TABLE reviews(

--    id INTEGER PRIMARY KEY AUTOINCREMENT,
--    title TEXT NOT NULL,
--    reveiw TEXT NOT NULL,
--    image_name TEXT NOT NULL,
--    cretor_id
--);

UPDATE reviews SET image_name = 'JPEG_Dog.jpeg'  WHERE title = 'review 1 title'
