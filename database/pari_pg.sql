CREATE DATABASE IF NOT EXISTS pari_pg CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pari_pg;

CREATE TABLE IF NOT EXISTS settings (
 id INT PRIMARY KEY,
 brand VARCHAR(100) NOT NULL,
 phone VARCHAR(50) NOT NULL,
 email VARCHAR(150) NOT NULL,
 address VARCHAR(255) NOT NULL,
 hero_eyebrow VARCHAR(255) NOT NULL,
 hero_title_line1 VARCHAR(255) NOT NULL,
 hero_title_highlight VARCHAR(255) NOT NULL,
 hero_title_line2 VARCHAR(255) NOT NULL,
 hero_description TEXT NOT NULL,
 hero_image TEXT NOT NULL,
 happy_residents VARCHAR(20) NOT NULL,
 room_count VARCHAR(20) NOT NULL,
 rating VARCHAR(20) NOT NULL,
 map_url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rooms (
 id INT AUTO_INCREMENT PRIMARY KEY,
 title VARCHAR(120) NOT NULL,
 room_type VARCHAR(50) NOT NULL,
 price VARCHAR(50) NOT NULL,
 tag VARCHAR(50) DEFAULT '',
 image_url TEXT NOT NULL,
 description TEXT NOT NULL,
 beds INT DEFAULT 1,
 meta TEXT DEFAULT '',
 features TEXT DEFAULT '',
 available INT DEFAULT 0,
 active TINYINT(1) DEFAULT 1,
 sort_order INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS facilities (
 id INT AUTO_INCREMENT PRIMARY KEY,
 title VARCHAR(120) NOT NULL,
 icon VARCHAR(20) DEFAULT '✓',
 active TINYINT(1) DEFAULT 1,
 sort_order INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS gallery (
 id INT AUTO_INCREMENT PRIMARY KEY,
 title VARCHAR(150) DEFAULT '',
 image_url TEXT NOT NULL,
 active TINYINT(1) DEFAULT 1,
 sort_order INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS testimonials (
 id INT AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 role VARCHAR(100) DEFAULT '',
 rating INT DEFAULT 5,
 text TEXT NOT NULL,
 avatar VARCHAR(20) DEFAULT '',
 active TINYINT(1) DEFAULT 1,
 sort_order INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS faqs (
 id INT AUTO_INCREMENT PRIMARY KEY,
 question VARCHAR(255) NOT NULL,
 answer TEXT NOT NULL,
 active TINYINT(1) DEFAULT 1,
 sort_order INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS contact_messages (
 id INT AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 email VARCHAR(150) NOT NULL,
 phone VARCHAR(20) NOT NULL,
 message TEXT NOT NULL,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO settings (id,brand,phone,email,address,hero_eyebrow,hero_title_line1,hero_title_highlight,hero_title_line2,hero_description,hero_image,happy_residents,room_count,rating,map_url)
VALUES (1,'Pari Pg','+91 98765 43210','paripg@gmail.com','Near Jagat Farm, Beta 1, B-132, Greater Noida','SAFE • COMFORTABLE • AFFORDABLE','Your','Second','Home in the City','A clean, secure and comfortable PG for students and working professionals with all modern facilities.','https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=1400&q=85','100+','30+','4.8','https://www.google.com/maps/search/?api=1&query=Pari+PG+Beta+1+Greater+Noida')
ON DUPLICATE KEY UPDATE id=id;

INSERT INTO rooms(title,room_type,price,tag,image_url,description,beds,meta,features,available,sort_order) VALUES
('Single Sharing','single','₹8,000','Popular','https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=900&q=85','A private, comfortable room designed for residents who want extra privacy, study space and a peaceful stay.',1,'1 Bed,Private Room,Study Table,WiFi','Single Bed,Study Table,Wardrobe,High-Speed WiFi,Charging Point,Housekeeping',1,1),
('Double Sharing','double','₹6,000','Best Choice','https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=900&q=85','A spacious shared room with two comfortable beds, dedicated study space and plenty of storage.',2,'2 Beds,2 Study Tables,Wardrobe,WiFi','2 Beds,Study Tables,Wardrobe,High-Speed WiFi,Charging Points,Housekeeping',3,2),
('Triple Sharing','triple','₹5,000','Budget Friendly','https://images.unsplash.com/photo-1560185008-b033106af5c3?auto=format&fit=crop&w=900&q=85','A budget-friendly room for three residents with practical furniture, storage and a comfortable setup.',3,'3 Beds,3 Study Tables,Wardrobe,WiFi','3 Beds,Study Tables,Wardrobe,High-Speed WiFi,Charging Points,Housekeeping',2,3)
ON DUPLICATE KEY UPDATE id=id;

INSERT INTO facilities(title,icon,sort_order) VALUES
('Fully Furnished Rooms','🛏',1),('Nutritious Meals','🍴',2),('High Speed WiFi','⌁',3),('24/7 Security','◉',4),('Laundry Service','▣',5),('Regular Cleaning','✦',6),('Power Backup','☼',7),('RO Water Purifier','💧',8),('Common Area','▰',9),('Parking Facility','P',10);

INSERT INTO gallery(title,image_url,sort_order) VALUES
('PG Exterior','https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=700&q=80',1),
('Single Room','https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=700&q=80',2),
('Double Room','https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=700&q=80',3),
('Triple Room','https://images.unsplash.com/photo-1560185008-b033106af5c3?auto=format&fit=crop&w=700&q=80',4),
('Dining Area','https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=700&q=80',5),
('Kitchen','https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=700&q=80',6),
('Common Area','https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=700&q=80',7),
('Living Area','https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=700&q=80',8),
('Bathroom','https://images.unsplash.com/photo-1600607688969-a5bfcd646154?auto=format&fit=crop&w=700&q=80',9),
('Laundry','https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=700&q=80',10),
('Outdoor','https://images.unsplash.com/photo-1598902108854-10e335adac99?auto=format&fit=crop&w=700&q=80',11),
('Garden','https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=700&q=80',12);

INSERT INTO testimonials(name,role,rating,text,avatar,sort_order) VALUES
('Rohan Sharma','Student',5,'Pari PG feels like home. The rooms are clean, food is good and the staff is very supportive.','RS',1),
('Priya Verma','Working Professional',5,'Safe, comfortable and in a prime location. Highly recommended for working professionals.','PV',2),
('Aman Singh','Student',5,'Great environment, good food and fast WiFi. Best PG experience in the city.','AS',3);

INSERT INTO faqs(question,answer,sort_order) VALUES
('What is the monthly rent?','The monthly rent depends on the room type. Check the Rooms section for current pricing.',1),
('Can I visit the PG before booking?','Yes. Contact us to schedule a visit and room tour before making a booking.',2),
('Is food included in the rent?','Food plans can be discussed with the PG management. Contact us for the current meal plan.',3),
('Is there a washing machine?','Yes, laundry facilities are available for residents.',4),
('What are the security arrangements?','The property provides CCTV coverage, controlled entry and 24/7 security support.',5),
('Are there any hidden charges?','We explain rent and applicable charges before booking. Ask our team for the current terms.',6),
('Is WiFi available in all rooms?','Yes, high-speed WiFi is available throughout the property.',7),
('What is the lock-in period?','The lock-in period depends on the selected stay plan. Confirm it with the management before booking.',8);
