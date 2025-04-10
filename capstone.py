import sqlite3
import bcrypt
from datetime import datetime, date
import csv


# *****************CREATE DATABASE******************************
def create_schema(cursor):
    with open("competency_tracker.txt", "r") as readfile:
        read_tables = readfile.read()
        cursor.executescript(read_tables)

connection = sqlite3.connect("competency_tracker_database.db")
cursor = connection.cursor()

create_schema(cursor)


# *****************USER LOGIN FUNCTION**************************
def user_login():
    print("User login:")
    email = input("\nEmail Address:\n")
    password_1 = input("\nPassword:\n")

    cursor.execute("SELECT user_id, password, user_type FROM Users WHERE email = ?", (email,))
    user_1 = cursor.fetchone()


    if user_1:
        user_id_1, hashed_password_1, user_type_1 = user_1
        if bcrypt.checkpw(password_1.encode('utf-8'), hashed_password_1):
            if user_type_1.lower() == "user":
                print("You have been logged in successfully!\n")
                return user_id_1
            else:
                print("\nAccess denied. You are not an authorized as a User.\n")
        else:
            print("Invalid password. Please try again.")
    else:
        print("\nEmail not found. Please try again.\n")
    

# ********************MANAGER LOGIN FUNCTION***************
def manager_login():
    print("\nManager Login:\n")
    email = input("Email Address:\n")
    password = input("Password:\n")

    cursor.execute("SELECT user_id, password, user_type FROM Users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user:
        user_id, hashed_password, user_type = user
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            if user_type.lower() == "manager":
                print("\nYou have been logged in as a manager.\n")
                return user_id
            else:
                print("\nAccess denied. You are not authorized as a manager.\n")
        else:
            print("\nInvalid password. Please try again.\n")
    else:
        print("\nEmail not found. Please try again.\n")

    return None



# # ***************LOGOUT FUNCTION***************************
# def logout():
#     # confirm = input("\nPress [L] again to be logged out and return to the main menu:\n").lower()
#     if confirm == "l":
#         print("You have been logged out")
#         return None
#     else:
#         print("\n Invalid entry. Please enter 'L' to logout.\n")
#         logout()


# *******************USER FUNCTION**************************
def user():
    user_id = user_login()
    if not user_id:
        return
    print(f"Welcome, User {user_id}!")
    
    while True:
        person = input("""
\nWhat would you like to do?\n
Press [1] to view your competency and assessment data
Press [2] to edit your first name
Press [3] to edit your last name
Press [4] to edit your phone number
Press [5] to edit your email address
Press [6] to edit your password
Press [L] to logout
""")
        if person == "1":
            rows = cursor.execute("SELECT * FROM AssessmentResults WHERE user_id = ?", (user_id,)).fetchall()
            if rows:
                print(f"\nAssessment Results for User ID {user_id}:\n")
                for row in rows:
                    print (row)
            else:
                print(f"\nNo assessment results found for User ID {user_id}.")
        
        elif person == "2":
            new_first_name = input("\nPlease enter a new first name:\n")
            cursor.execute("UPDATE Users SET first_name = ? WHERE user_id = ?", (new_first_name, user_id,))
            connection.commit()
            print("First name updated successfully.")
        
        elif person == "3":
            new_last_name = input("\nPlease enter a new last name:\n")
            cursor.execute("UPDATE Users SET last_name = ? WHERE user_id = ?", (new_last_name, user_id,))
            connection.commit()
            print("Last name successfully updated.")
        
        elif person == "4":
            while True:
                new_phone = input("\nPlease enter a new 10-digit phone number (numbers only):\n")
                if new_phone.isdigit() and len(new_phone) == 10:
                    break
                else:
                    print("Invalid phone number. Please enter exactly 10 digits.")

            cursor.execute("UPDATE Users SET phone = ? WHERE user_id = ?", (new_phone, user_id,))
            connection.commit()
            print("Phone number updated successfully.")

        
        elif person == "5":
            new_email = input("\nPlease enter a new email address:\n")
            cursor.execute("UPDATE Users SET email = ? WHERE user_id = ?", (new_email, user_id,))
            connection.commit()
            print("Email updated successfully.")
        
        elif person == "6":
            new_password = input("\nPlease enter a new password:\n")
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            cursor.execute("UPDATE Users SET password = ? WHERE user_id = ?", (hashed_password, user_id,))
            connection.commit()
            print("Password updated successfully.")
        
        elif person.lower() == "l":
            print("\nYou have been logged out")
            return None
        else:
            print("\n Invalid entry. Please enter 1, 2, 3, 4, 5, 6 or L for logout.\n")
            return



# ******************MANAGER FUNCTION************************
def the_manager():
    manager_id = manager_login()
    if not manager_id:
        return
    print(f"Welcome, Manager {manager_id}!")
    
    while True:
        person = input("""
\nWhat would you like to do?\n
Press [1] to view all users
Press [2] to search for users by first or last name
Press [3] to view a report of all users and their competency levels for a given competency
Press [4] to view a competency level report for an individual user
Press [5] to view a list of assessments for a given user
Press [6] to add a user, a new competency, a new assessment to a competency, or an assessment result for a user
Press [7] to edit a user's information, a competency, an assessment, or an assessment result
Press [8] to delete an assessment result
Press [9] to view a User Competency Summary
Press [10] to view Competency Results for all Users
Press [11] to Export or Import a CSV file
Press [L] to logout\n
""")
        if person == "1":
            rows = cursor.execute("SELECT user_id, first_name, last_name, phone, email, active FROM Users").fetchall()
            print("\nUser List:")
            print(f"{'ID':<5} {'Name':<25} {'Phone':<15} {'Email':<35} {'Active':<10}")
            print("-" * 90)
            for row in rows:
                full_name = f"{row[1]} {row[2]}"
                print(f"{row[0]:<5} {full_name:<25} {row[3]:<15} {row[4]:<35} {row[5]:<10}")
        
        elif person == "2":
            search_name = input("Enter first or last name to search:").lower()
            rows_2 = cursor.execute("SELECT * FROM Users WHERE LOWER(first_name) = ? OR LOWER(last_name) = ?", (search_name, search_name,)).fetchall()
            if rows_2:
                for row_2 in rows_2:
                    print("\n-----------------------------------")
                    print(f"User ID:       {row_2[0]}")
                    print(f"Name:          {row_2[1]} {row_2[2]}")
                    print(f"Phone:         {row_2[3]}")
                    print(f"Email:         {row_2[4]}")
                    print(f"Password:      (hidden)")
                    print(f"Active Status: {row_2[6]}")
                    print(f"Date Created:  {row_2[7]}")
                    print(f"Hire Date:     {row_2[8]}")
                    print(f"User Typer:    {row_2[9]}")
                print("-----------------------------------\n")
            else:
                print("No user found with that name.")
        
        elif person == "3":
            assessment_id = input("Enter the competency ID: ")
            rows_3 = cursor.execute("SELECT user_id, score From AssessmentResults WHERE assessment_id = ?", (assessment_id,)).fetchall()
            if rows_3:
                print("User ID   Cometency Level")
                print("----------------------------")
                for row_3 in rows_3:
                    print(f"{row_3[0]:<8} {row_3[1]}")
            else:
                print("Invalid ID or No results for the competency ID.")
        
        elif person == "4":
            user_id = input("Enter the user ID to view a competency level report for a person: ")
            rows_4 = cursor.execute("SELECT assessment_id, score FROM AssessmentResults WHERE user_id = ?", (user_id,)).fetchall()
            if rows_4:
                print("Assessment ID   Score")
                print("-" * 25)
                for row_4 in rows_4:
                    print(f"{row_4[0]:<15} {row_4[1]:>5}")
            else:
                print("Incorrect User ID.")
        
        elif person == "5":
            person_id = input("Enter the user ID to view a list of assessents for a given user: ")
            rows_5 = cursor.execute("SELECT assessment_id FROM AssessmentResults WHERE user_id = ?", (person_id,)).fetchall()
            if rows_5:
                print("\nAssessments List:")
                print("----------------------------")
                for row_5 in rows_5:
                    print(row_5[0])
            else:
                print("Incorrect User ID or no assessments found.")
        
        elif person == "6":
            add()
        
        elif person == "7":
            edit()
        
        elif person == "8":
            result_id = input("Enter the result ID number for the assessment result you wish to delete: ")
            cursor.execute("DELETE FROM AssessmentResults WHERE result_id = ?", (result_id,))
            connection.commit()
            if cursor.rowcount > 0:
                print("Assessment result has been deleted.")
            else:
                print("Incorrect result ID or no matching record found.")

        elif person == "9":
            the_user_id = input("\nEnter the User ID to view that User's Competency Summary:\n")

            rows_1 = cursor.execute("SELECT first_name, last_name, email FROM Users WHERE user_id = ?", (the_user_id,)).fetchall()
            print(f"{'Name':<30} {'Email':<30}")
            print("-" * 60)
            for row_1 in rows_1:
                full_name = f"{row_1[0]} {row_1[1]}"
                print(f"{full_name:<30} {row_1[2]:<30}")

            another_rows = cursor.execute("""
                SELECT a.name, ar.score, ar.date_taken
                FROM AssessmentResults ar
                JOIN Assessments a ON ar.assessment_id = a.assessment_id
                WHERE ar.user_id = ?
                AND ar.date_taken = (
                    SELECT MAX(date_taken)
                    FROM AssessmentResults
                    WHERE user_id = ar.user_id AND assessment_id = ar.assessment_id
                )
            """, (the_user_id,)).fetchall()

            print(f"\n{'Assessment Name':<50} {'Score':<10} {'Date Taken':<15}")
            print("-" * 75)
            for other_row in another_rows:
                print(f"{other_row[0]:<50} {other_row[1]:<10} {other_row[2]:<15}")

            average_score = cursor.execute("SELECT AVG(score) FROM AssessmentResults WHERE user_id = ?", (the_user_id,)).fetchone()[0]

            if average_score is not None:
                print(f"\n**Average Competency Score for ALL Competencies taken: {average_score:.2f}")
            else:
                print("\nInvalid User ID or No assessment results found for this user.")

        elif person == "10":
            the_assessment_id = input("\nEnter the Assessment ID to view a Competency Results Summary for all Users:\n")

            competency_info = cursor.execute("""
                SELECT c.name
                FROM Competencies c
                JOIN Assessments a ON c.competency_id = a.competency_id
                WHERE a.assessment_id = ?
            """, (the_assessment_id,)).fetchone()

            if competency_info:
                print(f"\nCompetency: {competency_info[0]}")
            else:
                print(f"\nNo such competency found for this Assessment ID.")

            avg_score = cursor.execute("""
                SELECT AVG(
                    CASE
                        WHEN ar.score IS NULL THEN 0
                        ELSE ar.score
                    END
                )
                FROM AssessmentResults ar
                JOIN Assessments a ON ar.assessment_id = a.assessment_id
                JOIN Users u ON ar.user_id = u.user_id
                WHERE a.assessment_id = ? AND u.active = 1
            """, (the_assessment_id,)).fetchone()[0]

            if avg_score is not None:
                print(f"\nAverage Competency Score: {avg_score:.2f}")
            else:
                print("\nAverage Competency Score: N/A (No scores found)")


            rows = cursor.execute("""
                SELECT u.first_name, u.last_name, 
                    CASE
                        WHEN ar.score IS NULL THEN 0
                        ELSE ar.score
                    END AS score,
                    CASE
                        WHEN ar.assessment_id IS NULL THEN ''
                        ELSE a.name
                    END AS assessment_name,
                    CASE
                        WHEN ar.date_taken IS NULL THEN ''
                        ELSE ar.date_taken
                    END AS date_taken
                FROM Users u
                LEFT JOIN AssessmentResults ar ON u.user_id = ar.user_id
                LEFT JOIN Assessments a ON ar.assessment_id = a.assessment_id
                WHERE a.assessment_id = ? AND u.active = 1
                AND ar.date_taken = (
                    SELECT MAX(date_taken)
                    FROM AssessmentResults
                    WHERE user_id = u.user_id AND assessment_id = a.assessment_id
                )
            """, (the_assessment_id,)).fetchall()

            print(f"\n{'Name':<30} {'Competency Score':<20} {'Assessment':<50} {'Date Taken':<15}")
            print("-" * 115)

            for row in rows:
                full_name = f"{row[0]} {row[1]}"
                print(f"{full_name:<30} {row[2]:<20} {row[3]:<50} {row[4]:<15}")

        elif person == "11":
            csv_files = input("""
        \nWhich would you like to do?\n
        Press [1] to Export a Users CSV File
        Press [2] to Export an Assessments CSV File
        Press [3] to Import an Assessments Results CSV File
        """)
            if csv_files == "1":
                export_users_to_csv("competency_tracker_database.db", "exported_user_data.csv")

            elif csv_files == "2":
                export_assessments_to_csv("competency_tracker_database.db", "exported_assessment_data.csv")

            elif csv_files == "3":
                import_assessment_results()
        
        elif person.lower() == "l":
                print("\nYou have been logged out")
                return None
        else:
            print("\n Invalid entry. Please enter 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 or L for logout.\n")
            return
        

# ****************ADD FUNCTION***********************
def add():
    while True:
        manager = input("""
\nWhat would you like to add?\n
Press [1] to add a user
Press [2] to add a new competency
Press [3] to add a new assessment to a competency
Press [4] to add an assessment result for a user for an assessment
Press [5] to exit\n
""")
        if manager == "1":
            input("\nPlease fill out the form below to create a new user:\n(Press 'Enter' to begin)\n-----------------------------------------\n\n")
    
            first_name = input("First Name   :")
            last_name = input("Last Name    :")

            while True:
                phone = input("Phone (10 digits): ")
                if phone.isdigit() and len(phone) == 10:
                    break
                else:
                    print("Invalid phone number. Please enter exactly 10 digits.")

            email = input("Email        :")
            password = input("Password     :")

            while True:
                try:
                    active = int(input("Active (enter '1') or Inactive (enter '0'): "))
                    if active in [0, 1]:
                        break
                    else:
                        print("Please enter '1' for active or '0' for inactive.")
                except ValueError:
                    print("Please enter a valid number (1 or 0).")

            date_created = date.today()

            while True:
                hire_date = input("Hire Date (YYYY-MM-DD): ")
                try:
                    datetime.strptime(hire_date, '%Y-%m-%d')
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")

            while True:
                user_type = input("User Type (User or Manager): ").strip().capitalize()
                if user_type in ["User", "Manager"]:
                    break
                else:
                    print("Invalid user type. Please enter either 'User' or 'Manager'.")


            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            create_person = "INSERT INTO Users (first_name, last_name, phone, email, password, active, date_created, hire_date, user_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"    
            cursor.execute(create_person, (first_name, last_name, phone, email, hashed_password, active, date_created, hire_date, user_type))
            connection.commit()
            print("\n\nThe User Record has been created.\n")
        
        elif manager == "2":
            input("\nPlease fill out the form below to create a new competency:\n(Press 'Enter' to begin)\n--------------------------------\n\n")

            name = input("Name of competency: ")
            day_created = date.today().isoformat()

            create_competency = "INSERT INTO Competencies (name, date_created) VALUES (?, ?)"
            cursor.execute(create_competency, (name, day_created,))
            connection.commit()
            print("\n\nThe competency has been created.\n")
        
        elif manager == "3":
            input("\nPlease fill out the form below to add a new assessment to a competency:\n(Press 'Enter' to begin)\n--------------------------------\n\n")

            name_1 = input("Name of assessment:             ")
            the_day_created = date.today().isoformat()
            competency_id = input("Enter the competency ID number: ")

            competency_exists = cursor.execute("SELECT COUNT(1) FROM Competencies WHERE competency_id = ?", (competency_id,)).fetchone()[0]

            if competency_exists:
                create_assessment = "INSERT INTO Assessments (name, date_created, competency_id) VALUES (?, ?, ?)"
                cursor.execute(create_assessment, (name_1, the_day_created, competency_id,))
                connection.commit()
                print("The assessment has been added to the competency.\n")
            else:
                print("Error: The provided competency ID does not exist. Please enter a valid competency ID.")
        
        elif manager == "4":
            input("""
            \nPlease fill out the form below to add an assessment result for a user for an assessment.
            \nFor Score please enter:
            \n0 for - No competency - Needs Training and Direction
            \n1 for - Basic Competency - Needs Ongoing Support
            \n2 for - Intermediate Competency - Needs Occasional Support
            \n3 for - Advanced Competency - Completes Task Independently
            \n4 for - Expert Competency - Can Effectively pass on this knowledge and can initiate optimizations
            \n(Press 'Enter' to begin)\n--------------------------------\n\n""")

            while True:
                user_id = input("User ID:                 ")
                result = cursor.execute(
                    "SELECT COUNT(1) FROM Users WHERE user_id = ? AND LOWER(user_type) = 'user'",
                    (user_id,)
                ).fetchone()[0]
                if result:
                    break
                else:
                    print("Error: User ID is either invalid or not associated with a regular User. Please enter a valid User ID.")

            while True:
                assessment_id = input("Assessment ID:           ")
                assessment_exists = cursor.execute("SELECT COUNT(1) FROM Assessments WHERE assessment_id = ?", (assessment_id,)).fetchone()[0]
                if assessment_exists:
                    break
                else:
                    print("Error: Assessment ID does not exist. Please enter a valid Assessment ID.")

            valid_scores = {'0', '1', '2', '3', '4'}
            score = input("Score (0-4):             ")
            while score not in valid_scores:
                print("Invalid score. Please enter a valid score between 0 and 4.")
                score = input("Score (0-4):             ")

            while True:
                the_date_taken = input("Date taken (YYYY-MM-DD): ")
                try:
                    the_date_taken = datetime.strptime(the_date_taken, "%Y-%m-%d").date().isoformat()
                    break
                except ValueError:
                    print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

            while True:
                manager_id = input("Manager ID:              ")
                result = cursor.execute(
                    "SELECT COUNT(1) FROM Users WHERE user_id = ? AND LOWER(user_type) = 'manager'",
                    (manager_id,)
                ).fetchone()[0]
                if result:
                    break
                else:
                    print("Error: Manager ID is either invalid or not associated with a Manager. Please enter a valid Manager ID.")

            create_assessment_results = """
                INSERT INTO AssessmentResults (user_id, assessment_id, score, date_taken, manager_id)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(create_assessment_results, (user_id, assessment_id, score, the_date_taken, manager_id,))
            connection.commit()
            print("The assessment results for the user have been added.")
        
        elif manager == "5":
            print("Exiting....")
            break

        else:
            print("Invalid selection. Please enter a valid option.")


# ***************EDIT FUNCTION*****************
def edit():
    while True:
        managers = input("""
\nWhat would you like to do?\n
Press [1] to edit a user's information
Press [2] to edit a competency
Press [3] to edit an assessment
Press [4] to edit an assessment result
Press [5] to exit
""")
        if managers == "1":
            person_id = input("\nPlease enter the user ID of the person of whose information you'd like to edit:\n")

            user_data = cursor.execute("SELECT * FROM Users WHERE user_id = ?", (person_id,)).fetchone()
            if not user_data:
                print("Error: User ID not found.")
                return
            while True:
                edit_user_menu = input("""
    \nWhich personal info would you like to edit?\n
    Press [1] to edit first name
    Press [2] to edit last name
    Press [3] to edit phone number
    Press [4] to edit email address
    Press [5] to edit active status (0 or 1)
    Press [6] to edit the date the person was created
    Press [7] to edit the date the person was hired
    Press [8] to edit the person type (Manager or User)
    Press [9] to exit
    """)
                if edit_user_menu == "1":
                    new_first_name = input("Please enter new first name:")
                    cursor.execute("UPDATE Users SET first_name = ? WHERE user_id = ?", (new_first_name, person_id,))
                    connection.commit()
                    print("First name updated successfully!")
                
                elif edit_user_menu == "2":
                    new_last_name = input("Please enter new last name:")
                    cursor.execute("UPDATE Users SET last_name = ? WHERE user_id = ?", (new_last_name, person_id,))
                    connection.commit()
                    print("Last name updated successfully!")
                
                elif edit_user_menu == "3":
                    while True:
                        new_phone = input("Please enter new phone number: ")
                        if new_phone.isdigit() and len(new_phone) == 10:
                            cursor.execute("UPDATE Users SET phone = ? WHERE user_id = ?", (new_phone, person_id,))
                            connection.commit()
                            print("Phone number updated successfully!")
                            break
                        else:
                            print("Invalid phone number. Please enter exactly 10 digits (numbers only).")


                elif edit_user_menu == "4":
                    new_email = input("Please enter new email:")
                    cursor.execute("UPDATE Users SET email = ? WHERE user_id = ?", (new_email, person_id,))
                    connection.commit()
                    print("Email address updated successfully!")
                
                elif edit_user_menu == "5":
                    while True:
                        new_active_status = input("Please enter 0 to deactivate a user, or 1 to activate a user:")
                        if new_active_status in ["0", "1"]:
                            cursor.execute("UPDATE Users SET active = ? WHERE user_id = ?", (new_active_status, person_id,))
                            connection.commit()
                            print("Active status updated successfully!")
                            break
                        else:
                            print("\nInvalid entry. Please enter a 0 or 1")
                
                elif edit_user_menu == "6":
                    while True:
                        new_date_created = input("Please enter a new date the user was created (YYYY-MM-DD):")
                        try:
                            new_date_created = datetime.strptime(new_date_created, "%Y-%m-%d").date()
                            break
                        except ValueError:
                            print("\nInvalid date format. Please enter the date in YYYY-MM-DD format.\n")
                    new_date_created = new_date_created.isoformat()
                    cursor.execute("UPDATE Users SET date_created = ? WHERE user_id = ?", (new_date_created, person_id,))
                    connection.commit()
                    print("\nDate created updated successfully!")
                
                elif edit_user_menu == "7":
                    while True:
                        new_hire_date = input("Please enter a new hire date for the user (YYYY-MM-DD):")
                        try:
                            new_hire_date = datetime.strptime(new_hire_date, "%Y-%m-%d").date().isoformat()
                            break
                        except ValueError:
                            print("\nInvalid date format. Please enter the date in YYYY-MM-DD format.\n")
                    cursor.execute("UPDATE Users SET hire_date = ? WHERE user_id = ?", (new_hire_date, person_id,))
                    connection.commit()
                    print("Hire date updated successfully!")
                
                elif edit_user_menu == "8":
                    while True:
                        new_user_type = input("Please enter Manager or User for user type:").lower()
                        if new_user_type in ["manager", "user"]:
                            cursor.execute("UPDATE Users SET user_type = ? WHERE LOWER(user_id) = ?", (new_user_type, person_id.lower()))
                            connection.commit()
                            print("User type updated successfully!")
                            break
                        else:
                            print("\nInvalid entry. Please enter 'manager' or 'user'.")

                elif edit_user_menu == "9":
                    print("Exiting edit user info menu....")
                    break

                else:
                    print("Invalid selection. Please enter a valid option.")

        elif managers == "2":
            while True:
                competency_id = input("\nPlease enter the competency ID of the competency you'd like to edit:\n")

                competency_data = cursor.execute("SELECT * FROM Competencies WHERE competency_id = ?", (competency_id,)).fetchone()
                
                if not competency_data:
                    print("Error: Competency ID not found. Please try again.")
                    continue 
                
                while True:
                    edit_competency_menu = input("""
                    \nWhich competency info would you like to edit?\n
                    Press [1] to edit name of competency
                    Press [2] to edit the date the competency was created
                    Press [3] to exit
                    """)

                    if edit_competency_menu == "1":
                        new_name = input("Please enter new competency name:")
                        cursor.execute("UPDATE Competencies SET name = ? WHERE competency_id = ?", (new_name, competency_id,))
                        connection.commit()
                        print("Competency name updated successfully!")

                    elif edit_competency_menu == "2":
                        while True:
                            new_day_created = input("Please enter new date for when the competency was created (YYYY-MM-DD):")
                            try:
                                new_day_created = datetime.strptime(new_day_created, "%Y-%m-%d").date().isoformat()
                                break
                            except ValueError:
                                print("\nInvalid date format. Please enter the date in YYYY-MM-DD format.\n")
                        cursor.execute("UPDATE Competencies SET date_created = ? WHERE competency_id = ?", (new_day_created, competency_id,))
                        connection.commit()
                        print("Competency creation date updated successfully!")

                    elif edit_competency_menu == "3":
                        print("Exiting edit competency menu......")
                        break

                    else:
                        print("Invalid selection. Please enter a valid option.")

        
        elif managers == "3":
            while True:
                assessment_id = input("\nPlease enter the assessment ID of the assessment you'd like to edit:\n")
                assessment_data = cursor.execute("SELECT * FROM Assessments WHERE assessment_id = ?", (assessment_id,)).fetchone()

                if not assessment_data:
                    print("Error: Assessment ID not found. Please try again.")
                    continue

                while True:
                    edit_assessment_menu = input("""
        \nWhich assessment info would you like to edit?\n
        Press [1] to edit name of assessment
        Press [2] to edit the date the assessment was created
        Press [3] to edit the competency ID connected to the assessment
        Press [4] to exit
        """)
                    if edit_assessment_menu == "1":
                        new_assessment_name = input("Please enter new assessment name:")
                        cursor.execute("UPDATE Assessments SET name = ? WHERE assessment_id = ?", (new_assessment_name, assessment_id,))
                        connection.commit()
                        print("Assessment name updated successfully!")

                    elif edit_assessment_menu == "2":
                        while True:
                            new_assessment_date_created = input("Please enter new date for when the assessment was created (YYYY-MM-DD):")
                            try:
                                new_assessment_date_created = datetime.strptime(new_assessment_date_created, "%Y-%m-%d").date().isoformat()
                                break
                            except ValueError:
                                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                        cursor.execute("UPDATE Assessments SET date_created = ? WHERE assessment_id = ?", (new_assessment_date_created, assessment_id,))
                        connection.commit()
                        print("Assessment creation date updated successfully!")

                    elif edit_assessment_menu == "3":
                        while True:
                            competency_id_1 = input("Please enter a new competency ID to link with this assessment:")
                            list_of_comp_ids = cursor.execute("SELECT competency_id FROM Competencies").fetchall()
                            if (int(competency_id_1),) in list_of_comp_ids:
                                cursor.execute("UPDATE Assessments SET competency_id = ? WHERE assessment_id = ?", (competency_id_1, assessment_id,))
                                connection.commit()
                                print("Competency ID has been updated for this assessment.")
                                break
                            else:
                                print("Error: Competency ID not found. Please try again.")

                    elif edit_assessment_menu == "4":
                        print("Exiting edit an assessment menu......")
                        break

                    else:
                        print("Invalid selection. Please enter a valid option.")

                if edit_assessment_menu == "4":
                    break
        
        
        elif managers == "4":
            while True:
                result_id = input("\nPlease enter the result ID of the assessment result you'd like to edit: \n")

                result_data = cursor.execute("SELECT * FROM AssessmentResults WHERE result_id = ?", (result_id,)).fetchone()
                if not result_data:
                    print("Error: Assessment Result ID not found.")
                    continue

                while True:
                    edit_result_menu = input("""
                \nWhich assessment result info would you like to edit?\n
                Press [1] to edit the user ID (must be a valid user ID)
                Press [2] to edit the assessment ID (must be a valid assessment ID)
                Press [3] to edit the assessment score (must be between 0 and 4)
                Press [4] to edit the date the assessment was taken (YYYY-MM-DD)
                Press [5] to edit the manager ID for this assessment result (must be a valid manager ID)
                Press [6] to exit
                """)

                    if edit_result_menu == "1":
                        while True:
                            person_id_1 = input("\nPlease enter a new User ID for this assessment result (must be a valid user ID): ")
                            list_of_person_ids = cursor.execute("SELECT user_id FROM Users WHERE user_type = 'user'").fetchall()
                            if (int(person_id_1),) in list_of_person_ids:
                                cursor.execute("UPDATE AssessmentResults SET user_id = ? WHERE result_id = ?", (person_id_1, result_id,))
                                connection.commit()
                                print("\nUser ID has been updated.\n")
                                break
                            else:
                                print("\nError: User ID not found.\n")

                    elif edit_result_menu == "2":
                        while True:
                            assessment_id_1 = input("\nPlease enter a new Assessment ID for this assessment result (must be a valid Assessment ID):\n")
                            list_of_assessment_ids = cursor.execute("SELECT assessment_id FROM Assessments").fetchall()
                            if (int(assessment_id_1),) in list_of_assessment_ids:
                                cursor.execute("UPDATE AssessmentResults SET assessment_id = ? WHERE result_id = ?", (assessment_id_1, result_id,))
                                connection.commit()
                                print("\nAssessment ID has been updated.\n")
                                break
                            else:
                                print("\nError: Assessment ID not found.\n")

                    elif edit_result_menu == "3":
                        while True:
                            assessment_score = input("\nPlease enter a new score for this assessment result (must be between 0 and 4):")
                            if assessment_score in ["0", "1", "2", "3", "4"]:
                                cursor.execute("UPDATE AssessmentResults SET score = ? WHERE result_id = ?", (assessment_score, result_id,))
                                connection.commit()
                                print("\nScore has been updated.\n")
                                break
                            else:
                                print("\nInvalid entry. Please enter a number between 0 and 4.\n")

                    elif edit_result_menu == "4":
                        while True:
                            edit_assessment_date_created = input("Please enter new date for when the assessment was taken (YYYY-MM-DD):")
                            try:
                                edit_assessment_date_created = datetime.strptime(edit_assessment_date_created, "%Y-%m-%d").date().isoformat()
                                break
                            except ValueError:
                                print("\nInvalid date format. Please enter the date in YYYY-MM-DD format.\n")

                        cursor.execute("UPDATE AssessmentResults SET date_taken = ? WHERE result_id = ?", (edit_assessment_date_created, result_id,))
                        connection.commit()
                        print("\nAssessment date taken updated successfully!\n")

                    elif edit_result_menu == "5":
                        while True:
                            manager_id = input("\nPlease enter a new Manager ID for this assessment result (must be a valid Manager ID):")
                            list_of_manager_ids = cursor.execute("SELECT user_id FROM Users WHERE user_type LIKE 'manager'").fetchall()
                            print("List of manager ids",list_of_manager_ids)
                            if (int(manager_id),) in list_of_manager_ids:
                                cursor.execute("UPDATE AssessmentResults SET manager_id = ? WHERE result_id = ?", (manager_id, result_id,))
                                connection.commit()
                                print("\nManager ID has been updated.\n")
                                break
                            else:
                                print("\nError: Manager ID not found.\n")

                    elif edit_result_menu == "6":
                        print("\nExiting edit assessment result menu....\n")
                        break

                    else:
                        print("\nInvalid selection. Please enter a valid option.\n")

                if edit_result_menu == "6":
                    break

        
        elif managers == "5":
            print("\nExiting edit menu....\n")
            break

        else:
            print("\nInvalid selection. Please enter a valid option.\n")


# ************EXPORT USERS CSV FILE**********************************
def export_users_to_csv(db_name, filename):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    with open(filename, 'w', newline= '') as csv_file:
        writer = csv.writer(csv_file)

        cursor.execute("SELECT user_id, first_name, last_name, email FROM Users")
        rows = cursor.fetchall()
        writer.writerow(["User ID", "First Name", "Last Name", "Email"])
        writer.writerows(rows)
        writer.writerow([])

    connection.close()
    print(f"Exported to {filename} successfully!")


# ************EXPORT ASSESSMENTS CSV FILE**********************************
def export_assessments_to_csv(db_name, filename):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    with open(filename, 'w', newline= '') as csv_file:
        writer = csv.writer(csv_file)

        cursor.execute("SELECT assessment_id, name, competency_id FROM Assessments")
        rows = cursor.fetchall()
        writer.writerow(["Assessment ID", "Assessment Name", "Competency ID associated with this assessment"])
        writer.writerows(rows)

    connection.close()
    print(f"Exported to {filename} successfully!")


# *****************CREATE CSV FILE FOR CSV IMPORT********************
def create_assessment_results_csv():
    headers = ['user_id', 'assessment_id', 'score', 'date_taken', 'manager_id']

    data = [5, 11, 4, '1999-05-12', 1]
    data_2 =[5, 8, 3, '1999-05-12', 1]
    
    with open('assessment_results.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        writer.writerow(headers)
        writer.writerow(data)
        writer.writerow(data_2)

    print("CSV file 'assessment_results.csv' created successfully.")

create_assessment_results_csv()


# *************CSV IMPORT****************************************
def import_assessment_results():
    filename = 'assessment_results.csv'
    db_name = "competency_tracker_database.db"

    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        with open(filename, 'r', newline='') as csv_file:
            reader = csv.DictReader(csv_file)

            required_columns = ['user_id', 'assessment_id', 'score', 'date_taken', 'manager_id']
            if not all(column in reader.fieldnames for column in required_columns):
                print("CSV file is missing one or more required columns: 'user_id', 'assessment_id', 'score', 'date_taken', 'manager_id'")
                return

            for row in reader:
                user_id = int(row['user_id'])
                assessment_id = row['assessment_id']
                score = int(row['score'])
                date_taken = row['date_taken']
                manager_id = int(row['manager_id'])

                cursor.execute("""
                    SELECT result_id FROM AssessmentResults
                    WHERE user_id = ? AND assessment_id = ?
                """, (user_id, assessment_id))
                existing = cursor.fetchone()

                if existing:
                    cursor.execute("""
                        UPDATE AssessmentResults
                        SET score = ?, date_taken = ?, manager_id = ?
                        WHERE user_id = ? AND assessment_id = ?
                    """, (score, date_taken, manager_id, user_id, assessment_id))
                else:
                    cursor.execute("""
                        INSERT INTO AssessmentResults (user_id, assessment_id, score, date_taken, manager_id)
                        VALUES (?, ?, ?, ?, ?)
                    """, (user_id, assessment_id, score, date_taken, manager_id))

        connection.commit()
        print(f"CSV data successfully imported into {db_name}!")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()




print("\n\n*** Competency Tracking Tool ***\n------------------------------------------")
while True:
    person = input("""
Are you a user or a manager?
Press [1] for User 
Press [2] for Manager 
Press [Q] to Quit\n
""").lower()
    

    if person == "1":
        user()
    elif person == "2":
        the_manager()
    elif person == "q":
        print("\nGoodbye!")
        break
    else:
        print("\nInvalid entry. Please enter 1, 2, or Q\n")
        continue