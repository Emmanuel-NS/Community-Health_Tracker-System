import os  # For operating system operations like clearing screen
import mysql.connector  # For MySQL database connectivity
import time  # For adding delays and timing operations
from datetime import datetime  # For handling date and time operations
import getpass  # For secure password input without displaying characters
from tabulate import tabulate  # For creating formatted tables in console
import re  # For regular expression operations (password validation)
from hashlib import sha256  # For password hashing
import keyboard  # For keyboard input detection

# MySQL Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  # Database server location
        user="root",  # Database username
        password="",  # Database password (empty in this case)
        database="health_tracker"  # Name of the database to connect to
    )

def clear_screen():
    # Clear the terminal screen.
    os.system('cls' if os.name == 'nt' else 'clear')  # Use 'cls' for Windows, 'clear' for Unix/Linux

class AdvancedHealthTracker:
    def __init__(self):
        # Initialize the tracker with necessary database connection.
        self.db_connection = get_db_connection()  # Establish database connection
        self.cursor = self.db_connection.cursor()  # Create database cursor for operations
        self.username = None  # Store current user's username
        self.display_welcome_message()  # Show welcome screen
        self.initialize_health_tips()  # Set up health tips database
        self.login_attempts=0   # Track failed login attempts
        
    
    def display_welcome_message(self):
        # Display an enhanced interactive welcome message.
        clear_screen()  # Clear terminal for clean display

        # Decorative header
        print("\n" + "═" * 70)
        print("║" + " " * 20 + "COMMUNITY HEALTH TRACKER" + " " * 20 + "║")
        print("═" * 70 + "\n")


        # Welcome messages and features list
        welcome_messages = [
                "🌟 Welcome to Your Personal Health Management System! 🌟",
                "\nAbout Our Application:",
                "We help you maintain and improve your health through:",
                "\n🏥 Health Monitoring & Tracking",
                "   • Log your daily health metrics",
                "   • Monitor weight, blood pressure, and activity",
                "   • View your health history",
                "\n💪 Personalized Health Advice",
                "   • Get customized health tips",
                "   • Receive symptom-specific advice",
                "   • Access health recommendations",
                "\n👩‍⚕️ Contact a Doctor",
                "   • Connect with specialized doctors based on your needs",
                "   • Access doctor contact information and advice",
                "\n📊 Features Available:",
                "   • User Registration and Login",
                "   • Health Metrics Logging",
                "   • Health Tips and Advice",
                "   • Personal Health History",
                "   • Progress Tracking",
                "   • Contact a Doctor"
            ]


        # Displaying welcome message with typing effects
        for message in welcome_messages:
            if keyboard.is_pressed("enter"): # Allow skipping animation
                break
            self.print_slowly(message, 0.03)  # Show message with typing effect

        # Show loading animation
        print("\nLoading your health companion", end='')
        for _ in range(3):
            time.sleep(0.5)
            print(".", end='', flush=True)
        print("\n")
        
        input("Press Enter to begin your health journey...") # Wait for user input
        clear_screen()


    def initialize_health_tips(self):
        # Initialize health tips database.
        self.health_tips = {
            "general": [  # General health advice
                "Stay hydrated by drinking at least 8 glasses of water daily.",
                "Aim for 7-9 hours of sleep each night.",
                "Practice good posture throughout the day.",
                "Take regular breaks from screen time.",
                "Stay socially connected with friends and family."
            ],
            "nutrition": [  # Nutrition specific advice
                "Include a variety of fruits and vegetables in your diet.",
                "Choose whole grains over refined grains.",
                "Limit processed foods and added sugars.",
                "Eat protein-rich foods with each meal.",
                "Practice mindful eating.",
                "Plan your meals ahead."
                "Include healthy fats in your diet, such as those from avocados, nuts, seeds, and olive oil."
            ],
            "exercise": [  # Exercise-related tips
                "Aim for 30 minutes of moderate exercise daily.",
                "Include both cardio and strength training.",
                "Take regular walking breaks.",
                "Try different types of physical activities.",
                "Start with gentle exercises if you're new to working out.",
                "Remember to stretch before and after exercise."
            ],
            "metrics": {  # Metric-specific health advice
                "weight": [  # Weight-related tips
                    "Maintain a healthy weight by balancing your calorie intake and expenditure.",
                    "If you're overweight, aim for gradual weight loss with a balanced diet and exercise."
                ],
                "blood_pressure": [  # Blood pressure tips
                    "Monitor your blood pressure regularly and aim for a healthy range.",
                    "If you have high blood pressure, reduce salt intake and stay physically active."
                ],
                "steps": [  # step count tips
                    "Aim for at least 10,000 steps daily to maintain a healthy lifestyle.",
                    "Take breaks during long periods of sitting to improve circulation."
                ]
            }
        }

    def get_health_tips(self, category="general", user_metrics=None):
      """ Get health tips by category, optionally based on your health metrics."""
        if user_metrics:  # If specific metrics are provided(Return relevant metric-based tips)
            # Provide tips based on the user's health metrics
            if 'weight' in user_metrics:
                return self.health_tips["metrics"]["weight"]
            if 'blood_pressure' in user_metrics:
                return self.health_tips["metrics"]["blood_pressure"]
            if 'steps' in user_metrics:
                return self.health_tips["metrics"]["steps"]
        
        # Default that general health tips if no metrics are available
        return self.health_tips.get(category, self.health_tips["general"])  # Return general category tips if no specific metrics

    def show_tips(self, tips):
        """Display the health tips."""
        print()
        for tip in tips:  # Display tip with bullet point
            print(f"* {tip}")
            
        input("\nPress Enter to continue...")  # Wait for user acknowledgment
        self.show_health_tips_menu()  # Return health tips menu

    def show_health_tips_menu(self):
        """Show health tips menu."""
        clear_screen()
        # Display menu options
        print("Health Tips Menu:")
        print("1. General Tips")
        print("2. Nutrition Tips")
        print("3. Exercise Tips")
        print("4. Back to Home")  # User can go back to home menu
        choice = input("Select an option: ")

        # Handle user choice
        if choice == '1':
            tips = self.get_health_tips("general")
            self.show_tips(tips)
        elif choice == '2':
            tips = self.get_health_tips("nutrition")
            self.show_tips(tips)
        elif choice == '3':
            tips = self.get_health_tips("exercise")
            self.show_tips(tips)
        elif choice == '4' or choice == '0': 
            print("back to home ...")
            time.sleep(1) # Handle '0' and '4' to go back to Home menu
            self.show_home_menu()  # Go back to the home menu
        else:
            print("Invalid choice. Please try again.")
            self.show_health_tips_menu()


    def print_slowly(self, text, delay=0.05):
        """Print text with a typing effect."""
        for char in text:
            if keyboard.is_pressed("enter"):  # Allow skipping
                break
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def log_health_metrics(self, weight, blood_pressure, steps):
        """Log user's health metrics in the MySQL database."""
        try:
            # Convert and validate inputs
            weight = float(weight)
            steps = int(steps)
            
            # Validate blood pressure format
            if not blood_pressure.count('/') == 1:
                return False, "Blood pressure must be in format '120/80'"

            # Parse and validate blood pressure values
            sys_bp, dia_bp = map(int, blood_pressure.split('/'))
            if not (60 <= sys_bp <= 200 and 40 <= dia_bp <= 130):
                return False, "Blood pressure values are out of normal range"

            # Get user ID
            self.cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
            user = self.cursor.fetchone()
            if not user:
                return False, "User not found!"
            
            user_id = user[0]

            # Insert health metrics into database
            self.cursor.execute(
                "INSERT INTO health_data (user_id, weight, blood_pressure, steps) VALUES (%s, %s, %s, %s)",
                (user_id, weight, blood_pressure, steps)
            )
            self.db_connection.commit()
            return True, "Health metrics logged successfully!"
        except ValueError:
            return False, "Please enter valid numbers!"
        except mysql.connector.Error as err:
            return False, f"Error saving health data: {err}"
        
    def log_health_metrics_menu(self):
        """Log health metrics."""
        weight = input("Enter your weight (kg): ")
        blood_pressure = input("Enter your blood pressure (e.g., 120/80): ")
        steps = input("Enter the number of steps you took today: ")

        # Try to log the metrics
        success, message = self.log_health_metrics(weight, blood_pressure, steps)
        print(message)
        time.sleep(2)
        if success:
            input("\nPress Enter to return to the home menu.")
            self.show_home_menu()
        else:
            retry = input("Would you like to try again? (y/n): ")
            if retry.lower() == 'y':
                self.log_health_metrics_menu()
            else:
                print("back to home ...")
                time.sleep(1)
                self.show_home_menu()

    def display_health_history(self):
        """Display user's health history from the database in a tabular format."""
        # Get user ID
        self.cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
        user = self.cursor.fetchone()
        if not user:
            return [],[], "User not found!"
        
        user_id = user[0]
        # Retrieve health data ordered by date
        self.cursor.execute(
            "SELECT date_logged, weight, blood_pressure, steps FROM health_data WHERE user_id = %s ORDER BY date_logged DESC",
            (user_id,)
        )
        health_data = self.cursor.fetchall()
        if not health_data:
            return [],[], "No health history found!"
        
        # Prepare data for tabulation (table display)
        table_data = []
        for data in health_data:
            table_data.append([
                data[0],  # Date
                f"{data[1]} kg",  # Weight
                data[2],  # Blood Pressure
                data[3]  # Steps
            ])
        
        # Create headers
        headers = ["Date of Entry", "Weight", "Blood Pressure", "Steps"]
        
        return table_data, headers, "Health history !!!"

    def view_health_history(self):
        """View health history."""
        history, headers, message = self.display_health_history()
        print(message)
        
        if history:
            # Use tabulate to create a nicely formatted table
            print(tabulate(history, headers=headers, tablefmt="grid"))

        input("\nPress Enter to continue...")
        self.show_home_menu()
    
    def validate_password(self, password):
        """We have to ensure that the password is strong."""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long!"
        if not re.search(r"\d", password):
            return False, "Password must contain at least one number!"
        if not re.search(r"[A-Za-z]", password):
            return False, "Password must contain at least one letter!"
        return True, "Password is strong."

    def login_user(self, username, password):
        """Log in a user by validating their credentials."""
        self.cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = self.cursor.fetchone()
        if not user:
            return False, "Username not found!, try again!..."

        # Verify password
        stored_password = user[0]
        if sha256(password.encode()).hexdigest() != stored_password:
            return False, "Incorrect password!, try again!..."
        
        self.username = username
        return True, "Login successful!"

    def login(self):
        """Log in an existing user."""
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")  # Hide password input
        success, message = self.login_user(username, password)
        
        print(message)
        time.sleep(2)
        if success:
            self.show_home_menu()
        else:
            if self.login_attempts < 2:  # Allow 3 attempts total
                print()
                print(f"try again!!, you still have {3-(self.login_attempts + 1)} attempts:")
                self.login_attempts = self.login_attempts + 1
                self.login()
            else:
                print("\nSorry, you have failed to login many times, may be you're not official user!!!\n")
                time.sleep(3)
                self.print_slowly("Closing System ...",0.3)
                time.sleep(1)
                clear_screen()
                exit()

    def register_user(self, username, password, is_doctor=False, specialty=None, name=None, email=None, tel=None):
        """Register a new user or doctor in the MySQL database with hashed password."""
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long!"
        
        self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if self.cursor.fetchone():
            return False, "Username already exists!"
        
        valid_password, msg = self.validate_password(password)
        if not valid_password:
            return False, msg
        
        password_hash = sha256(password.encode()).hexdigest()

        try:
            if is_doctor:
                # Insert doctor with specialty
                self.cursor.execute("INSERT INTO doctors (name,specialty,email,phone,username, password) VALUES (%s, %s, %s,%s,%s,%s)", 
                                    (name,specialty,email,tel,username, password_hash))
            else:
                # Insert general user
                self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                                    (username, password_hash))
            self.db_connection.commit()
            return True, "Registration successful!"
        except mysql.connector.Error as err:
            return False, f"Error saving user data: {err}"

    def register(self):
        """Register a new user or doctor."""
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")
        is_doctor = input("Are you a doctor? (y/n): ").lower() == 'y'
        specialty = None

        if is_doctor:
            specialty = self.show_specialties()
            name=input("enter your Full name: ")
            email=input("enter your email: ")
            tel=input("enter your phone number: ")
            success, message = self.register_user(username, password, is_doctor, specialty,name,email,tel)
        else:
            success, message = self.register_user(username, password)

        print(message)

        if success:
            terminate = input("Registration complete. Do you want to login now? (y/n): ").lower()
            if not is_doctor and terminate == 'y':
                time.sleep(1)
                self.show_home_menu()
            else:
                self.show_login_menu()
        else:
            terminate = input("Registration failed. Do you want to try again? (y/n): ").lower()
            if terminate == 'n':
                print("Registration cancelled. Returning to the main menu.")
                self.show_login_menu()
            else:
                self.register()

    def show_login_menu(self):
        """Show login/register menu."""
        clear_screen()
        print("hello there! choose (1) to login or (2) to register new account")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            self.login()
        elif choice == '2':
            self.register()
        elif choice == '3':
            print("You have chosen to exit. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please try again.")
            self.show_login_menu()

    def show_home_menu(self):
        """Display the home menu."""
        clear_screen()
        print("Welcome to Health Tracker!")
        print("1. Health Tips")
        print("2. Log Health Metrics")
        print("3. View Health History")
        print("4. Contact a Doctor")
        print("5. Logout")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            self.show_health_tips_menu()
        elif choice == '2':
            self.log_health_metrics_menu()
        elif choice == '3':
            self.view_health_history()
        elif choice == '4':
            self.contact_doctor()
        elif choice == '5':
            self.logout()
        elif choice == '6':
            print("You have chosen to exit. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please try again.")
            self.show_home_menu()
    
    def show_specialties(self):
        """Display a list of specialties for doctors to choose from."""
        specialties = [
            "Cardiology",
            "Dermatology",
            "Neurology",
            "Orthopedics",
            "Pediatrics",
            "Psychiatry",
            "General Medicine"
        ]
        
        print("\nSpecialties available for Doctors:")
        for idx, specialty in enumerate(specialties, start=1):
            print(f"{idx}. {specialty}")
        
        choice = int(input("\nSelect a specialty by number: "))
        if 1 <= choice <= len(specialties):
            return specialties[choice - 1]
        else:
            print("Invalid choice. Please try again.")
            return self.show_specialties()

    def contact_doctor(self):
        """Provide the user an option to contact specific doctors."""
        # Fetch doctors with more detailed information
        self.cursor.execute("SELECT id, name, specialty, email, phone FROM doctors")
        doctors = self.cursor.fetchall()
        
        if not doctors:
            print("No doctors are available at the moment.")
            input("\nPress Enter to return to the home menu.")
            self.show_home_menu()
            return
        
        # Prepare data for tabulation
        table_data = []
        for doctor in doctors:
            table_data.append([
                doctor[0],  # ID
                f"Dr. {doctor[1]}",  # Name
                doctor[2],  # Specialty
            ])
        
        # Headers for the table
        headers = ["ID", "Doctor Name", "Specialty"]
        
        # Display doctors in a table format
        print("\nAvailable Doctors:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        try:
            # Prompt for doctor selection
            doctor_id = int(input("\nEnter the ID of the doctor you wish to contact: "))
            
            # Validate doctor ID
            selected_doctor = next((doc for doc in doctors if doc[0] == doctor_id), None)
            
            if not selected_doctor:
                print("Invalid doctor ID. Please try again.")
                self.contact_doctor()
                return
            
            # Display selected doctor's contact information
            print("\nSelected Doctor's Contact Information:")
            print(f"Name: Dr. {selected_doctor[1]}")
            print(f"Specialty: {selected_doctor[2]}")
            print(f"Email: {selected_doctor[3]}")
            print(f"Phone: {selected_doctor[4]}")
        
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            self.contact_doctor()
        
        input("\nPress Enter to return to the home menu.")
        self.show_home_menu()

    def logout(self):
        """Logout user and return to login/registration."""
        self.username = None
        print("You have successfully logged out.")
        time.sleep(1)
        self.show_login_menu()

if __name__ == "__main__":
    tracker = AdvancedHealthTracker()
    tracker.show_login_menu()
