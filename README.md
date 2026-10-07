# Pari PG - Complete Flask + MySQL Dynamic Website

This is the complete frontend + Flask + MySQL version.

## Stack
- HTML
- CSS
- Vanilla JavaScript
- Flask
- MySQL

No PHP, React, Node, Vue or Django is required.

## Dynamic modules
The public website reads its main content from MySQL:
- Website settings / hero
- Rooms
- Facilities
- Gallery
- Testimonials
- FAQs
- Contact submissions

Admin can:
- View dashboard statistics
- Add/edit/delete rooms
- Add/edit/delete facilities
- Add/edit/delete gallery entries
- Add/edit/delete testimonials
- Add/edit/delete FAQs
- Edit website settings
- View/search/edit/delete contact submissions

## Setup on Windows + XAMPP
1. Start XAMPP MySQL only. Apache is not required.
2. Import `database/pari_pg.sql` in phpMyAdmin.
3. Copy `.env.example` to `.env`.
4. If XAMPP root password is blank, keep `DB_PASSWORD=` blank.
5. Open terminal in this project folder.
6. Run:
   python -m pip install -r requirements.txt
7. Run:
   python run.py
8. Website:
   http://127.0.0.1:5000/
9. Admin:
   http://127.0.0.1:5000/admin/

Default admin:
Username: admin
Password: admin123

Change admin credentials in `.env` before production.

## Important
The image fields currently use image URLs. The admin can change the URL for each image. A later image-upload module can be added if needed.

The contact form submits via JavaScript to Flask `/api/contact`; the browser stays on the website and shows success/error inside the form.
