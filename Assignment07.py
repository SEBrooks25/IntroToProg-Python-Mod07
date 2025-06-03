# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   SophiaBrooks, 06/03/2025, Edited Script
# ------------------------------------------------------------------------------------------ #

import json

# Constants
MENU: str = '''---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course
    2. Show current data  
    3. Save data to a file
    4. Exit the program
-----------------------------------------'''
FILE_NAME: str = "Enrollments.json"

# Variables
menu_choice: str = ""
students: list = []


# Data Classes
class Person:
    """Stores data about a person"""

    def __init__(self, first_name: str = "", last_name: str = ""):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        if not value.isalpha():
            raise ValueError("First name must contain only letters.")
        self._first_name = value.strip().title()

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        if not value.isalpha():
            raise ValueError("Last name must contain only letters.")
        self._last_name = value.strip().title()

    def __str__(self) -> str:
        return f"{self.first_name},{self.last_name}"


class Student(Person):
    """Stores data about a student (inherits Person)"""

    def __init__(self, first_name: str = "", last_name: str = "", course_name: str = ""):
        super().__init__(first_name, last_name)
        self.course_name = course_name

    @property
    def course_name(self) -> str:
        return self._course_name

    @course_name.setter
    def course_name(self, value: str):
        if not value:
            raise ValueError("Course name cannot be empty.")
        self._course_name = value.strip().title()

    def __str__(self) -> str:
        return f"{super().__str__()},{self.course_name}"

    def to_dict(self) -> dict:
        return {"first_name": self.first_name, "last_name": self.last_name, "course_name": self.course_name}


# Processing Classes
class FileProcessor:
    """Processes data to and from a file"""

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """Reads JSON data from file and fill student_data with Student objects"""
        try:
            with open(file_name, "r") as file:
                data = json.load(file)
                student_data.clear()
                for item in data:
                    student = Student(item["first_name"], item["last_name"], item["course_name"])
                    student_data.append(student)
        except FileNotFoundError:
            IO.output_error_messages("File not found; starting with an empty list.")
        except Exception as e:
            IO.output_error_messages("Error reading file.", e)

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """Writes student data to JSON file"""
        try:
            with open(file_name, "w") as file:
                json.dump([s.to_dict() for s in student_data], file)
        except Exception as e:
            IO.output_error_messages("Error writing to file.", e)


# Presentation Classes
class IO:
    """Performs input and output"""

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        print("ERROR:", message)
        if error:
            print("DETAILS:", error)

    @staticmethod
    def output_menu(menu: str):
        print(menu)

    @staticmethod
    def input_menu_choice() -> str:
        return input("Please enter your choice: ").strip()

    @staticmethod
    def input_student_data(student_data: list):
        try:
            first = input("Enter student's first name: ")
            last = input("Enter student's last name: ")
            course = input("Enter course name: ")
            student = Student(first, last, course)
            student_data.append(student)
        except Exception as e:
            IO.output_error_messages("Invalid input for student registration.", e)

    @staticmethod
    def output_student_courses(student_data: list):
        if not student_data:
            print("No student data available.")
        for student in student_data:
            print(student)


# Load existing data on start
FileProcessor.read_data_from_file(FILE_NAME, students)

# Menu Loop
while True:
    IO.output_menu(MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":
        IO.input_student_data(students)
    elif menu_choice == "2":
        IO.output_student_courses(students)
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(FILE_NAME, students)
    elif menu_choice == "4":
        print("Exiting the program. Goodbye!")
        break
    else:
        IO.output_error_messages("Invalid menu option. Please choose 1-4.")
