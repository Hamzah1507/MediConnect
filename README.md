# 🏥 MediConnect – Telemedicine & Online Pharmacy Website

MediConnect is a **Django-based Telemedicine and Online Pharmacy Platform** that allows users to search medicines by categories or names, add them to a shopping cart, and order them with doorstep delivery.  
It includes user authentication, cart management, and secure checkout with payment integration.

---

## 🚀 Features
- **User Authentication**
  - Signup & Login (Django Auth)
  - Session-based user management
- **Medicine Management**
  - Browse medicines by categories
  - Search medicines by name
  - View details (price, description, image)
- **Shopping Cart**
  - Add medicines to cart
  - Remove from cart
  - Automatic price calculation
- **Checkout & Payment**
  - Simple checkout flow
  - Easy payment integration (Stripe/Razorpay)
  - Delivery address entry
- **Order Flow**
  - Save orders with user details
  - Track order status (Pending → Shipped → Delivered)
- **Responsive UI**
  - Built with **HTML, CSS, and JavaScript**
  - Interactive and user-friendly

---

## 🛠️ Tech Stack
- **Backend:** Django 5.x, Python 3.12
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL
- **Authentication:** Django Auth
- **Payment Gateway:** (Razorpay/Stripe/PayPal – configurable)
- **Deployment:** Works locally with `runserver`

---

## 📂 Project Structure
mediconnect/
│── home/ # Main app (models, views, urls)
│ ├── migrations/
│ ├── templates/ # HTML templates
│ │ ├── base.html
│ │ ├── landing.html
│ │ ├── signin.html
│ │ ├── login.html
│ │ ├── cart.html
│ │ └── ...
│ ├── models.py # Medicine, Cart, Order models
│ ├── views.py # App logic (search, cart, checkout)
│ ├── urls.py # URL routing
│── mediconnect/
│ ├── settings.py
│ ├── urls.py
│── static/ # CSS, JS, Images
│── manage.py

yaml
Copy code

---
⚙️ Installation & Setup

1️⃣ Clone the repository
bash
git clone https://github.com/yourusername/mediconnect.git
cd mediconnect
2️⃣ Create a virtual environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Configure database
Update settings.py with your MySQL database details:

python
Copy code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mediconnect',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
5️⃣ Run migrations
bash
Copy code
python manage.py makemigrations
python manage.py migrate
6️⃣ Create a superuser (for admin access)
bash
Copy code
python manage.py createsuperuser
7️⃣ Run development server
bash
Copy code
python manage.py runserver 8000
Open browser at 👉 http://127.0.0.1:8000/

🧪 Usage
Register a new user or login.

Browse/search medicines by name or category.

Add medicines to cart.

Open Cart → Review items, remove if needed.

Proceed to Checkout and pay.

Wait for doorstep delivery 🚚

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss.

📜 License

This project is licensed under the MIT License – see the LICENSE
 file for details.
