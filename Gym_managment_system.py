import mysql.connector
import getpass
import datetime




class GymDB:
   
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1119", 
                database="gymdb",
                auth_plugin="mysql_native_password"
            )
            self.cursor = self.db.cursor()
            print("MySQL connection successful")
            self.create_tables()
        except mysql.connector.Error as error:
            print(f"Error connecting to MySQL:{error}")

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id INT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            duration VARCHAR(50) NOT NULL,
            price DECIMAL(10,2) NOT NULL
        );""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS membership (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            gender VARCHAR(10) NOT NULL,
            contact BIGINT UNIQUE NOT NULL,
            password VARCHAR(30) NOT NULL,
            plan_id INT,
            join_date DATE,
            FOREIGN KEY (plan_id) REFERENCES plans(id) 
        );""") 
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            member_id INT NOT NULL,
            date DATE NOT NULL
        );""") 


        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS trainer (
            id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            fields VARCHAR(100),
            contact VARCHAR(15) 
        );""")

       
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );""")
        
        self.db.commit()
        print("All required tables are created successfully.") 

#       // only user plane

    def register_user(self):
        print("\n--- Register User ---")
        name = input('Enter your name to register :').strip()
        if not name or name.isdigit():
            print('Enter a valid name.')
            return
        email = input('Enter Your E-mail: ').strip()
        if '@' not in email or '.' not in email:
            print('Enter a valid E-mail address.')
            return
    
        self.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if self.cursor.fetchone():
            print('This E-mail is already registered.')
            return
        password = getpass.getpass('Create a password: ')
        if not password:
            print("Password cannot be empty.")
            return
        self.cursor.execute("INSERT INTO users (name, password, email) VALUES (%s, %s, %s)", (name, password, email))
        self.db.commit()
        print('User registration completed successfully.')
       

    def login_user(self):
        print("\n--- User Login ---")
        email = input('Enter your email: ').strip()
        if "@" not in email or "." not in email:
            print("Enter a valid email.")
            return 
        self.cursor.execute("SELECT id, name, password FROM users WHERE email=%s", (email,))
        result = self.cursor.fetchone()
        if result:
            name, password = result
            password = getpass.getpass("Enter your password: ")
            if password == result[2]:
                print(f"Welcome, {name}!") 
            else:
                print("Incorrect password.")
        else:
            print("Email not registered.")

# only admin plane
    def admin_login(self):
        print("\n--- Admin Login ---")
        username = input("Enter admin username: ").strip()
        password = getpass.getpass("Enter admin password: ")

        if username == "admin" and password == "12345":
            print("Admin login successful.")
            return True
        else:
            print("Invalid admin credentials.")
            return False

    def admin_menu(self):
        while True:
            print('\n_________________________________')
            print('        ----ADMIN MENU----')
            print('\n_________________________________')
            print('1. Manage Plans')
            print('3. Manage Trainers')
            print('4. View All Attendance')
            print('5. Register User')
            print('6. Log-out')
            print('_________________________________')

            choice = input('Enter your choice:').strip()
            if choice == "1":
                self.plans()
            elif choice == "2":
                self.manage_trainers()
            elif choice == "3":
                self.view_attendance()
            elif choice == "4":
                self.register_user()
            elif choice == "5":
                print("Log-Out.")
                break
            else:
                print("Invalid choice. Please try again.")


#  Plan management
    def plans(self):
        while True:
            print('\n--- Manage Plans ---')
            print('1. View All Plans')
            print('2. Add New Plan')
            print('3. Update Plan Details')
            print('4. Delete Plan')
            print('5. Back to Admin Menu')

            plan_choice = input('Enter your choice: ').strip()
            if plan_choice == '1':
                self.view_plans()
            elif plan_choice == '2':
                self.add_plan()
            elif plan_choice == '3':
                self.update_plan()
            elif plan_choice == '4':
                self.delete_plan()
            elif plan_choice == '5':
                break
            else:
                print("Invalid choice.")

    def view_plans(self):
   
        print("\n--- All Gym Plans ---")
    
        self.cursor.execute("SELECT id, name, duration, price FROM plans ORDER BY id")
        plans = self.cursor.fetchall()
        if not plans:
            print("No plans found.")
            return
        print(f"{'ID':<5} {'Name':<20} {'Duration':<15} {'Price':<10}")
        for plan in plans:
            print(f"{plan[0]:<5} {plan[1]:<20} {plan[2]:<15} ₹{plan[3]:<10.2}")
        

    def add_plan(self):
      
        print("\n--- Add New Plan ---")
        plan_id = input("Enter Plan ID: ").strip()
        if not plan_id.isdigit():
            print("Plan ID must be a number.")
            return
        plan_id = int(plan_id)

        plan_name = input("Enter Plan Name: ").strip()
        if not plan_name:
            print("Plan name cannot be empty.")
            return

        self.cursor.execute("SELECT id FROM plans WHERE name = %s", (plan_name,))
        if self.cursor.fetchone():
            print(f"A plan with the name '{plan_name}' already exists.")
            return
        duration = input("Enter Duration: ").strip()
        if not duration:
            print("Duration cannot be empty.")
            return
        price = input("Enter Price").strip()
        if not price.isdigit():
            print("Price must be a valid number.")
            return
        price = float(price)
        self.cursor.execute("INSERT INTO plans (id, name, duration, price) VALUES (%s, %s, %s, %s)",(plan_id, plan_name, duration, price))
        self.db.commit()
        print(f"Plan '{plan_name}' added successfully.")



    def update_plan(self):
        print("\n--- Update Plan ---")
        self.view_plans()
        plan_id = input("Enter the ID of the plan to update: ").strip()
        if not plan_id.isdigit():
            print("Plan ID must be a number.")
            return
        plan_id = int(plan_id)
        self.cursor.execute("SELECT * FROM plans WHERE id = %s", (plan_id,))
        if not self.cursor.fetchone():
            print(f"No plan found with ID {plan_id}.")
            return
        print("Enter new details:")
        new_name = input(f"New Plan Name (current: {plan_id}): ").strip() 
        new_duration = input("New Duration: ").strip()
        new_price_str = input("New Price: ").strip()

        updates = []
        values = []

        if new_name:
            self.cursor.execute("SELECT id FROM plans WHERE name = %s AND id != %s", (new_name, plan_id))
            if self.cursor.fetchone():
                print(f"This plan with the name '{new_name}' already exists.")
                return
            updates.append("name = %s")
            values.append(new_name)
        if new_duration:
            updates.append("duration = %s")
            values.append(new_duration)
        if new_price_str:
            if not new_price_str.isdigit():
                print("New price must be a valid number.")
                return
        updates.append("price = %s")
        values.append(float(new_price_str))
        if not updates:
            print("Plan is not updated.")
            return
        query = f"UPDATE plans SET {', '.join(updates)} WHERE id = %s"
        values.append(plan_id)
        self.cursor.execute(query, tuple(values))
        self.db.commit()
        print(f"Plan ID {plan_id} updated successfully.")



    def delete_plan(self):
        print("\n--- Delete Plan ---")
        self.view_plans()
        plan_id = input("Enter the ID plan to delete: ").strip()
        if not plan_id.isdigit():
            print("Plan ID must be a number.")
            return
        plan_id = int(plan_id)
        self.cursor.execute("SELECT name FROM plans WHERE id = %s", (plan_id,))
        plan_name_result = self.cursor.fetchone()
        if not plan_name_result:
            print(f"No plan found with ID {plan_id}.")
            return

        plan_name = plan_name_result[0]

        confirm = input(f"Are you sure you want to delete plan '{plan_name}' (ID: {plan_id})? (yes/no): ").lower().strip()
        if confirm != 'yes':
            print("Plan deletion cancelled.")
            return

        self.cursor.execute("DELETE FROM plans WHERE id = %s", (plan_id,))
        self.db.commit()
        print(f"Plan '{plan_name}' (ID: {plan_id}) deleted successfully.")




#  trainer management admin 

    def manage_trainers(self):
        while True:
            print('\n--- Manage Trainers ---')
            print('1. View All Trainers')
            print('2. Add New Trainer')
            print('3. Update Trainer Details')
            print('4. Delete Trainer')
            print('5. Back to Admin Menu')
            trainer_choice = input('Enter your choice: ').strip()

            if trainer_choice == '1':
                self.view_trainers()
            elif trainer_choice == '2':
                self.add_trainer()
            elif trainer_choice == '3':
                self.update_trainer()
            elif trainer_choice == '4':
                self.delete_trainer()
            elif trainer_choice == '5':
                break
            else:
                print("Invalid choice.")

    def add_trainer(self):
        print("\n--- Add New Trainer ---")
        
        trainer_id_str = input("Enter Trainer ID ").strip()
        if not trainer_id_str.isdigit():
            print("Trainer ID must be a number.")
            return
        trainer_id = int(trainer_id_str)

        name = input("Enter Trainer Name: ").strip()
        if not name or name.isdigit():
            print("Enter a valid name.")
            return

        workout_types= input("Enter our types of workout,(examle.,Weight Training, Yoga): ").strip()
        if not workout_types:
            print("cannot be empty.")
            return

        contact_str = input("Enter Contact Number : ").strip()
        if not contact_str.isdigit() or len(contact_str) != 10:
            print(" Contact number must be 10 digits.")
            return
        contact = contact_str 

        self.cursor.execute("SELECT id FROM trainer WHERE id = %s", (trainer_id,))
        if self.cursor.fetchone():
            print(f"Trainer with ID {trainer_id} already exists. Please use a unique ID.")
            return

        self.cursor.execute("SELECT id FROM trainer WHERE contact = %s", (contact,))
        if self.cursor.fetchone():
                print(f"Trainer with contact number {contact} already exists. Please use a unique contact.")
                return

        self.cursor.execute("INSERT INTO trainer (id, name, expertise, contact) VALUES (%s, %s, %s, %s)",(trainer_id, name, workout_types, contact))
        self.db.commit()
        print(f"Trainer '{name}' added successfully.")
    

    def view_trainers(self):
      
        print("\n--- All Trainers ---")
    
        self.cursor.execute("SELECT id, name, fields, contact FROM trainer ORDER BY id")
        trainers = self.cursor.fetchall()
        if not trainers:
            print(" No trainers found.")
            return

        print(f"{'ID':<5} {'Name':<20} {'fields':<25} {'Contact':<15}")
        for trainer in trainers:
            print(f"{trainer[0]:<5} {trainer[1]:<20} {trainer[2]:<25} {trainer[3]:<15}")
            print("--------------------------------------------------------------------")
       
    def update_trainer(self):
        print("\n--- Update Trainer ---")
        self.view_trainers() 
        trainer_id_str = input("Enter the  trainerID to update: ").strip()
        if not trainer_id_str.isdigit():
            print("Trainer ID must be a number.")
            return
        trainer_id = int(trainer_id_str)

        self.cursor.execute("SELECT * FROM trainer WHERE id = %s", (trainer_id,))
        trainer_data = self.cursor.fetchone()
        if not trainer_data:
            print(f"No trainer found with ID {trainer_id}.")
            return

        print("Enter new details:")
        new_name = input(f"New Name (current: {trainer_data[1]}): ").strip()
        new_fields = input(f"New fields (current: {trainer_data[2]}): ").strip()
        new_contact_str = input(f"New Contact Number (current: {trainer_data[3]}): ").strip()

        updates = []
        values = []

        if new_name:
            if new_name.isdigit():
                print("Invalid name. ")
                return
            updates.append("name = %s")
            values.append(new_name)
            if new_fields:
                updates.append("expertise = %s")
                values.append(new_fields)
            if new_contact_str:
                if not new_contact_str.isdigit() or len(new_contact_str) != 10:
                    print("Invalid contact number.")
                    return
            self.cursor.execute("SELECT id FROM trainer WHERE contact = %s AND id != %s", (new_contact_str, trainer_id))
            if self.cursor.fetchone():
                print(f"Contact number {new_contact_str} already belongs to another trainer.")
                return
            updates.append("contact = %s")
            values.append(new_contact_str)

            if not updates:
                print(" i No changes entered.")
                return

            query = f"UPDATE trainer SET {', '.join(updates)} WHERE id = %s"
            values.append(trainer_id)

            self.cursor.execute(query, tuple(values))
            self.db.commit()
            print(f"Trainer ID {trainer_id} updated successfully.")
        
    def delete_trainer(self):
       
        print("\n--- Delete Trainer ---")
        self.view_trainers() 
        trainer_id_str = input("Enter trainer ID to delete: ").strip()
        if not trainer_id_str.isdigit():
            print("Trainer ID must be a number.")
            return
        trainer_id = int(trainer_id_str)
        self.cursor.execute("SELECT name FROM trainer WHERE id = %s", (trainer_id,))
        trainer_name_result = self.cursor.fetchone()
        if not trainer_name_result:
            print(f"No trainer found with ID {trainer_id}.")
            return

        trainer_name = trainer_name_result[0]

        confirm = input(f"Are you sure you want to delete trainer '{trainer_name}' (ID: {trainer_id})? (yes/no): ").lower().strip()
        if confirm != 'yes':
            print("Trainer deletion cancelled.")
            return

        self.cursor.execute("DELETE FROM trainer WHERE id = %s", (trainer_id,))
        self.db.commit()
        print(f"Trainer '{trainer_name}' (ID: {trainer_id}) deleted successfully.")
        

    # ttendance management admin & member 

    def mark_attendance(self, member_id):
        current_date = datetime.date.today()

        self.cursor.execute("SELECT name FROM membership WHERE id = %s", (member_id,))
        member_name_result = self.cursor.fetchone()
        if not member_name_result:
            print(f"Member with ID {member_id} not found.")
            return
        
        member_name = member_name_result[0]
        self.cursor.execute("SELECT * FROM attendance WHERE member_id = %s AND date = %s", (member_id, current_date))
        if self.cursor.fetchone():
            print(f"⚠️ Attendance for {member_name} (ID: {member_id}) already marked for today ({current_date}).")
            return

        self.cursor.execute("INSERT INTO attendance (member_id, date) VALUES (%s, %s)", (member_id, current_date))
        self.db.commit()
        print(f"Attendance marked for {member_name} (ID: {member_id}) on {current_date}.")


    def view_attendance(self, member_id):
      
        print("\n--- Attendance Records ---")
       
        if member_id:
            query = """
                SELECT m.name, a.date
                FROM attendance a
                JOIN membership m ON a.member_id = m.id
                WHERE a.member_id = %s
                ORDER BY a.date ;
                """
            self.cursor.execute(query, (member_id,))
            attendance_records = self.cursor.fetchall()
            if not attendance_records:
                print(f"No attendance records found for member ID {member_id}.")
                return
            print(f"Attendance for Member ID: {member_id}")
            print(f"{'Name':<20} {'Date':<12}")
            
            for record in attendance_records:
                print(f"{record[0]:<20} {str(record[1]):<12}")
                print("---------------------------------------------------")
            else:
                query = """
                SELECT m.id, m.name, a.date
                FROM attendance a
                JOIN membership m ON a.member_id = m.id
                ORDER BY a.date , m.name ;
                """
                self.cursor.execute(query)
                attendance_records = self.cursor.fetchall()
                if not attendance_records:
                    print("No attendance records found.")
                    return
                print(f"{'Member ID':<12} {'Member Name':<20} {'Date':<12}")
                for record in attendance_records:
                    print(f"{record[0]:<12} {record[1]:<20} {str(record[2]):<12}")
                print("---------------------------------------------" )
  




#  Member panel functions 

    def member_login(self):

        print("\n--- Member Login ---")
        contact_str = input('Enter your 10-digit contact number: ').strip()
        if not contact_str.isdigit() or len(contact_str) != 10:
            print('Invalid contact number.')
            return 
        contact = int(contact_str)

        try:
            self.cursor.execute("SELECT id, name, password FROM membership WHERE contact=%s", (contact,))
            result = self.cursor.fetchone()
            if result:
                member_id, name, stored_password = result
                password = getpass.getpass("Enter your password: ")
                if password == stored_password:
                    print(f"Welcome, {name}!")
                    return
                else:
                    print("Incorrect password.")
            else:
                print("Member with this contact number not found.")
        except mysql.connector.Error as err:
            print(f"Error during member login: {err}")
        return 

    def member_menu(self, member_id):
        while True:
            print('\n_________________________________')
            print('          MEMBER MENU')
            print('_________________________________')
            print('1. Mark My Attendance')
            print('2. View My Attendance History')
            print('3. View My Details')
            print('4. Logout')
            print('_________________________________')

            choice = input('Enter your choice: ').strip()

            if choice == "1":
                self.mark_attendance(member_id)
            elif choice == "2":
                self.view_attendance(member_id=member_id)
            elif choice == "3":
                self.view_member_details(member_id)
            elif choice == "4":
                print("Log out from Member panel.")
                break
            else:
                print("Invalid choice. Please try again.")

    def view_member_details(self, member_id):
       
        print("\n--- My Details ---")
        try:
            query = """
            SELECT m.id, m.name, m.age, m.gender, m.contact, p.name AS plan_name, p.duration, p.price, m.join_date
            FROM membership m
            LEFT JOIN plans p ON m.plan_id = p.id
            WHERE m.id = %s;
            """
            self.cursor.execute(query, (member_id,))
            member = self.cursor.fetchone()

            if not member:
                print(f"Member with ID {member_id} not found.")
                return

            print(f"Member ID: {member[0]}")
            print(f"Name: {member[1]}")
            print(f"Age: {member[2]}")
            print(f"Gender: {member[3]}")
            print(f"Contact: {member[4]}")
            print(f"Join Date: {member[8]}")
            print("\n--- Current Plan ---")
            if member[5]:
                print(f"Plan Name: {member[5]}")
                print(f"Duration: {member[6]}")
                print(f"Price: {member[7]:.2f}")
            else:
                print("No active plan assigned.")
        except mysql.connector.Error as err:
            print(f"Error viewing member details: {err}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

#  Main  Logic

def main():
  
    gym_app = GymDB()

    while True:
        print('\n=================================')
        print('    GYM MANAGEMENT SYSTEM MENU')
        print('=================================')
        print('1. Admin Login')
        print('2. Member Login')
        print('3. Register User')
        print('4. Exit')
        print('=================================')

        choice = input('Enter your choice:').strip()

        if choice == "1":
            if gym_app.admin_login():
                gym_app.admin_menu()
        elif choice == "2":
            member_id = gym_app.member_login()
            if member_id:
                gym_app.member_menu(member_id)
        elif choice == "3":
            gym_app.register_user()
        elif choice == "4":
            print("Thank you for using the Gym Management System. Goodbye!")
            gym_app.cursor.close()
            gym_app.db.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


