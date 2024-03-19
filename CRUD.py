import psycopg2

# Gets all the student from the table
def getAllStudents(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students")
            print("\nstudent_id, first_name, last_name, email, enrollment_date")
            
            for record in cursor.fetchall():
                print(", ".join(map(str, record)))

            print("")
            
    except psycopg2.Error as e:
        connection.rollback()
        print("\nError retrieving the students from the database: \n", e)

# Create addStudent function
def addStudent(connection):
    try:
        first_name = input("\nEnter the first name of the student: ")
        last_name = input("Enter the last name of the student: ")
        email = input("Enter the email of the student: ")
        enrollment_date = input("Enter the enrollment date of the stuent (YYYY-MM-DD): ")
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)",
                           (first_name, last_name, email, enrollment_date))
            connection.commit()
        print("\nThe new student has been added to the database.\n")

    except psycopg2.Error as e:
        connection.rollback()
        print("\nError adding the student to the database:", e)

# Update the student's email
def updateStudentEmail(connection):
    try:
        student_id = input("\nEnter the Student ID you want to update: ")
        new_email = input("Enter the new email of the student: ")
        with connection.cursor() as cursor:
            cursor.execute("UPDATE students SET email = %s WHERE student_id = %s", (new_email, student_id))
            connection.commit()
        if cursor.statusmessage.split()[1] == '0':
            print(f"Could not find a student ID {student_id}\n")
        else:
            print(f"Student ID {student_id} email has been updated\n")

    except psycopg2.Error as e:
        print("\nError updating the student's email\n", e)

# Deleting a student from the database 
def deleteStudent(connection):
    try:
        student_id = input("\nEnter the ID of the student you want to delete: ")
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            connection.commit()
        if cursor.statusmessage.split()[1] == '0':
            print(f"Could not find a student ID {student_id}\n")
        else:
            print(f"Student ID {student_id} has been deleted\n")

    except psycopg2.Error as e:
        connection.rollback()
        print("\nError deleting the student: \n", e)

def main():
    
    database = input("\nEnter the database name: ")
    username = input("Enter the databse username: ")
    password = input("Enter the database password: ")

    with psycopg2.connect(dbname=database, user=username, password=password) as connection:

        print("\nSelect one of the following options:\n")
        print("    1. Get all of the students in the database")
        print("    2. Add a new student in the databse")
        print("    3. Update the email of a student in the databse")
        print("    4. Delete a student in the databse")
        print("    Press 0 to exit the program.\n")

        with connection.cursor() as cursor:
            while(not False):
                result = input("Option: ")
                result = result.upper()

                if(result == "0"):
                    break
                elif(result == "1"):
                    getAllStudents(connection)
                elif(result == "2"):
                    addStudent(connection)
                elif(result == "3"):
                    updateStudentEmail(connection)
                elif(result == "4"):
                    deleteStudent(connection)
                else:
                    print("Option entered is not valid.")

        print("\nThe database has disconnected.\n")
        
# main guard
if __name__ == "__main__":
    main()