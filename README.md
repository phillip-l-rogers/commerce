# 🛍️ Commerce

**Built for [CS50’s Web Programming with Python and JavaScript (CS50W)](https://cs50.harvard.edu/web/).**  
An eBay-style auction platform where users can list items, place bids, comment on listings, and manage watchlists.

---

## 🚀 Features

- User authentication (register, login, logout)
- Create auction listings with title, description, starting bid, category, and image
- Place bids and view current highest bidder
- Comment on listings
- Add/remove items from a personal watchlist
- Close listings and declare winner
- Browse active listings by category
- Responsive design using Bootstrap

---

## 🖼️ Screenshots

> *(Add screenshots here, or link to demo video)*

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite
- **Auth:** Django’s built-in authentication system

---

## 📦 Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/phillip-l-rogers/commerce.git
   cd commerce
Create and activate a virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Apply migrations:

bash
Copy
Edit
python manage.py migrate
Run the development server:

bash
Copy
Edit
python manage.py runserver
Visit:
http://127.0.0.1:8000/ in your browser.

🧪 Testing Tips
Register multiple users to simulate bidding interactions

Test tie-breakers by placing bids with equal value

Add, remove, and view items in your watchlist

Use the Django admin panel to verify database changes

📁 Project Structure
bash
Copy
Edit
commerce/
├── auctions/          # Main app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── manage.py
└── requirements.txt
📚 Acknowledgments
This project was completed as part of CS50W: Web Programming with Python and JavaScript

Built using the Django web framework and Bootstrap

📜 License
This project is for educational purposes and is not licensed for commercial use.
