# Student Grade Analyzer

students = []  # List of dictionaries: {"name": str, "grades": [int]}


def add_student():
    name = input("Enter student name: ").strip()

    # Check if student already exists
    for student in students:
        if student["name"].lower() == name.lower():
            print("This student already exists!")
            return

    students.append({"name": name, "grades": []})
    print(f"Student '{name}' added successfully.\n")


def add_grades():
    name = input("Enter student name: ").strip()

    # Find student
    for student in students:
        if student["name"].lower() == name.lower():
            print("Enter grades (0–100). Type 'done' to finish:")

            while True:
                grade_input = input("Enter a grade (or 'done'): ")

                if grade_input.lower() == "done":
                    break

                try:
                    grade = int(grade_input)
                    if 0 <= grade <= 100:
                        student["grades"].append(grade)
                    else:
                        print("Grade must be between 0 and 100.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            print("Grades updated.\n")
            return

    print("Student not found.\n")


def show_report():
    if not students:
        print("No students found.\n")
        return

    print("--- Student Report ---")

    averages = []

    for student in students:
        grades = student["grades"]

        try:
            avg = sum(grades) / len(grades)
            averages.append(avg)
            print(f"{student['name']}'s average grade is {avg:.1f}.")
        except ZeroDivisionError:
            print(f"{student['name']}'s average grade is N/A.")

    if averages:
        print(f"Max Average: {max(averages):.1f}")
        print(f"Min Average: {min(averages):.1f}")
        print(f"Overall Average: {sum(averages)/len(averages):.1f}")
    else:
        print("No grades available to calculate overall summary.")

    print()


def find_top_student():
    valid_students = [
        (s["name"], sum(s["grades"]) / len(s["grades"]))
        for s in students if s["grades"]
    ]

    if not valid_students:
        print("No students with grades available.\n")
        return

    top_name, top_avg = max(valid_students, key=lambda x: x[1])

    print(f"The top student is {top_name} with an average of {top_avg:.1f}.\n")


def main():
    while True:
        print("--- Student Grade Analyzer ---")
        print("1. Add a new student")
        print("2. Add grades for a student")
        print("3. Show report")
        print("4. Find top performer")
        print("5. Exit")
        
        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_student()
            elif choice == 2:
                add_grades()
            elif choice == 3:
                show_report()
            elif choice == 4:
                find_top_student()
            elif choice == 5:
                print("Exiting program.")
                break
            else:
                print("Invalid option. Try again.\n")

        except ValueError:
            print("Please enter a valid number.\n")


if __name__ == "__main__":
    main()
