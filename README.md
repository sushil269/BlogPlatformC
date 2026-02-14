# Full-Stack Blog Platform with Role-Based Access Control

## 📌 Project Motivation
While my academic foundation is in Physics, I developed this platform to master the complexities of backend architecture and secure data management. This project serves as a comprehensive demonstration of Full-Stack web development using the Django framework, focusing on user-role logic and responsive design.

## 🚀 Key Technical Features

### 1. Sophisticated Permission Logic (RBAC)
The core of this application is a custom Role-Based Access Control system that creates two distinct user experiences:
* **Authors:** Authorized to execute full administrative actions, including post creation, editing, and deletion, as well as moderating discussion threads.
* **Readers:** Secured access for registered users to browse content and engage through a threaded comment and reply system.

### 2. Dynamic Search & Content Discovery
Implemented a backend query engine that allows users to filter the blog repository by:
* Article Title
* Author Identity
* Content Keywords

### 3. Responsive Frontend Engineering
The interface is built with a focus on high readability and mobile responsiveness, utilizing a grid-based card layout that dynamically renders post snippets and author tags.

## 🛠 Technical Stack
* **Backend:** Python 3.x, Django MVT Framework
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
* **Database:** MySQL / SQLite
* **Authentication:** Django User Model & Custom Permission Mixins
* **Development Tools:** Git, VS Code, Postman

## 📁 Repository Overview
* `/blog`: Contains the core application logic, views, and URL routing.
* `/templates`: Custom HTML files for the Author Dashboard and Reader Feed.
* `/static`: CSS and JS assets for the responsive UI.

## 📸 Local Development
To run this project locally:
1. Clone the repository: `git clone https://github.com/sushil269/BlogPlatformC`
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`
