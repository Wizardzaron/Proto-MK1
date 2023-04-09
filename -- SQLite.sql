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


INSERT INTO reviews VALUES(1, 'The Mystery Meat Wrapped Nukalurk is absolutly delicious. The brown sugar mixed with the cumin spice really make the flaovers pop with the scallops. I was not able to find bacon though so I went to jacks place to get some of his meat. He always seem to have fresh meat available even though I dont see any cows or pigs, wonder where he gets it from?', 'Mystery Meat Wrapped Nukalurk')