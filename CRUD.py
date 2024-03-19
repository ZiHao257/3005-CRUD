import psycopg2

connection = None

# Connect to the database
def connect_to_database(database, username, password):
    global connection
    connection = psycopg2.connect(dbname=database, user=username, password=password)

# Gets all the student from the table
def getAllStudents():
    try:
        query = "SELECT * FROM students"
        with connection.cursor() as cursor:
            cursor.execute(query)
            print("\nstudent_id, first_name, last_name, email, enrollment_date")
            
            for record in cursor.fetchall():
                print(", ".join(map(str, record)))

            print("")
            
    except psycopg2.Error as e:
        connection.rollback()
        print("\nError retrieving the students from the database: \n", e)

# Create addStudent function
def addStudent(first_name, last_name, email, enrollment_date):
    try:
        query = "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)"
        values = (first_name, last_name, email, enrollment_date)
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            connection.commit()
        print("\nThe new student has been added to the database.\n")

    except psycopg2.Error as e:
        connection.rollback()
        print("\nError adding the student to the database:", e)

# Update the student's email
def updateStudentEmail(student_id, new_email):
    try:
        query = "UPDATE students SET email = %s WHERE student_id = %s"
        values = (new_email, student_id)
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            rows_affected = cursor.rowcount
            connection.commit()
        if(rows_affected == 1):
            print(f"Student ID {student_id} email has been updated\n")
        else:
            print(f"Could not find a student ID {student_id}\n")

    except psycopg2.Error as e:
        print("\nError updating the student's email\n", e)

# Deleting a student from the database 
def deleteStudent(student_id):
    try:
        query = "DELETE FROM students WHERE student_id = %s"
        values = (student_id,)
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            rows_affected = cursor.rowcount
            connection.commit()
        if(rows_affected == 0):
            print(f"Could not find a student with ID {student_id}\n")
        else:
            print(f"Student with ID {student_id} has been successfully deleted.\n")

    except psycopg2.Error as e:
        connection.rollback()
        print("\nError deleting the student.\n", e)

# main function 
def main():
    database = input("\nEnter the database name: ")
    username = input("Enter the database username: ")
    password = input("Enter the database password: ")

    connect_to_database(database, username, password)

    print("\nSelect one of the following options:\n")
    print("    Enter 1 to print all of the students in the database")
    print("    Enter 2 to add a new student into the database")
    print("    Enter 3 to to update the email of a student in the database")
    print("    Enter 4 to delete a student in the database")
    print("    Enter 0 to exit the program.\n")

    while(not False):
        
        result = input("Option: ").upper()
        
        if(result == "0"):
            break
        elif(result == "1"):
            getAllStudents()
        elif(result == "2"):
            first_name = input("\nEnter the first name of the student: ")
            last_name = input("Enter the last name of the student: ")
            email = input("Enter the email of the student: ")
            enrollment_date = input("Enter the enrollment date of the student (YYYY-MM-DD): ")
            addStudent(first_name, last_name, email, enrollment_date)
        elif(result == "3"):
            student_id = input("\nEnter the Student ID you want to update: ")
            new_email = input("Enter the new email of the student: ")
            updateStudentEmail(student_id, new_email)
        elif(result == "4"):
            student_id = input("\nEnter the ID of the student you want to delete: ")
            deleteStudent(student_id)
        else:
            print("Option entered is not valid.")

    print("\nThe database has disconnected.\n")
    connection.close()

# main function called
if __name__ == "__main__":
    main()
