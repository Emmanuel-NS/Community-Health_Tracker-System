# Community Health Tracker

A comprehensive health management system built with Python that allows users to track their health metrics, receive personalized health tips, and connect with healthcare professionals.

## 🌟 Features

- **User Authentication**
  - Secure login and registration system
  - Password hashing for enhanced security
  - Role-based access (Users and Doctors)

- **Health Monitoring**
  - Log daily health metrics including:
    - Weight
    - Blood pressure
    - Step count
  - View historical health data in a tabulated format
  - Track progress over time

- **Health Tips**
  - Access to categorized health advice:
    - General wellness tips
    - Nutrition guidance
    - Exercise recommendations
    - Metric-specific health advice

- **Doctor Directory**
  - Browse available healthcare professionals
  - View doctor specialties and contact information
  - Direct connection with healthcare providers

## 🔧 Prerequisites

- Python 3.x
- MySQL Server
- Required Python packages:
  ```
  mysql-connector-python
  tabulate
  keyboard
  ```

## ⚙️ Installation

1. Clone the repository or download the source code

2. Install required packages:
   ```bash
   pip install mysql-connector-python tabulate keyboard
   ```

3. Set up MySQL database:
   ```sql
   CREATE DATABASE health_tracker;
   USE health_tracker;

   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(255) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL
   );

   CREATE TABLE doctors (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       specialty VARCHAR(255) NOT NULL,
       email VARCHAR(255),
       phone VARCHAR(20),
       username VARCHAR(255) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL
   );

   CREATE TABLE health_data (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT,
       weight FLOAT,
       blood_pressure VARCHAR(10),
       steps INT,
       date_logged TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (user_id) REFERENCES users(id)
   );
   ```

4. Configure database connection:
   - Open the code and modify the `get_db_connection()` function with your MySQL credentials:
   ```python
   def get_db_connection():
       return mysql.connector.connect(
           host="localhost",
           user="your_username",
           password="your_password",
           database="health_tracker"
       )
   ```

## 🚀 Usage

1. Start the application:
   ```bash
   sudo python health_tracker.py
   ```

2. At the main menu, choose to either:
   - Login with existing credentials
   - Register a new account (as a user or doctor)

3. After logging in, you can:
   - View health tips in different categories
   - Log your daily health metrics
   - View your health history
   - Contact available doctors

## 🔐 Security Features

- Password hashing using SHA-256
- Input validation for all user inputs
- Limited login attempts (3 maximum)
- Secure password requirements:
  - Minimum 8 characters
  - Must contain at least one number
  - Must contain at least one letter

## 📝 Notes

- Blood pressure should be entered in the format "120/80"
- Weight should be entered in kilograms
- Steps should be entered as whole numbers
- Doctors must provide specialty and contact information during registration

## ⚠️ Error Handling

The application includes comprehensive error handling for:
- Invalid inputs
- Database connection issues
- Authentication failures
- Data validation errors

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements you make.


