# MyPage Web Application

MyPage is a Django-based web application that enables sellers to create product listings, showcase their products, and gather customer reviews. It provides an easy and responsive platform for both sellers and customers.

## Features

- **Seller Dashboard:** Sellers can log in, create, update, and delete product listings, view orders, and manage their shop.

- **User Authentication:** Secure user registration and login system.

- **Product Listings:** Easily add, edit, and remove product details such as title, description, price, and images.

- **Customer Reviews:** Shoppers can leave reviews and ratings for products they've purchased.

- **Responsive Design:** Ensures optimal user experience on various devices.

## Installation

Follow these steps to set up and run the MyPage project locally:

### Prerequisites

- Python 3.10.5
- Django 4.0.4
- Virtualenv (recommended)

### Clone the Repository

- git clone https://github.com/mezardini/mypage.git
- cd MyPage 
- virtualenv venv
- venv/bin/activate
- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver


## Usage
- To access the admin panel, go to http://127.0.0.1:8000/admin/ and log in with the superuser credentials.

- Sellers can create listings and manage their shops from the dashboard.

- Customers can browse listings, add products to their cart, and leave reviews.

## Contributing
- Contributions are welcome! Feel free to open issues or submit pull requests.
