from app import login
from random import randint
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


ACCESS = {
    'visitor' : 0,
    'student' : 1,
    'instructor' : 2,
    'registrar' : 3
}


class User(UserMixin):
    def __init__(self, username, password, access=ACCESS['student']):
        self.username = username
        self.email = ""
        self.password_hash = generate_password_hash(password)
        self.posts = []
        self.access = access


    def allowed(self, access_level):
        return self.access >= access_level

    def is_registrar(self):
        return (self.access == ACCESS['registrar'])

    def set_registrar(self):
        self.access = ACCESS['registrar']

    def set_instructor(self):
        self.access = ACCESS['instructor']

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def generate_StudentID(digits):
        student_id = ''.join(["{}".format(randint(0, 9)) for num in range(0, digits)])
        return student_id


    def __repr__(self):
        return '<User {}, Password {}>'.format(self.username,
                                               self.password_hash)

    @classmethod
    def get(cls, username):
        for user in registered_users_table:
            if username == user.username:
                return user
        print("User Not Found in DB")
        return None

    
    @property
    def id(self):
        return self.username



    
    class Complaint():
        def __init__(self, name, subject):
            self.name = name
            self.subject = subject
            self.content = None

        def set_complaint(self, content):
            self.content = content


        def __repr__(self):
            return '<Name {}\n, Subject {}\n, Content {}\n>'.format(self.name,
                                                                    self.subject,
                                                                    self.content)


class Student(User):
    def __init__(self, *args, **kwargs):
        super(Student, self).__init__(*args, **kwargs)
        self.student_id = User.generate_StudentID(8)
        self.grades = {}
        self.suspended = False
        self.terminated = False
        self.warning = 0
        self.overallGPA = 0
        self.gpaBySemester = []
        self.coursesBySemester = []


    def addGrade(self, courseID, grade, course, credits, year):
        self.grades[courseID] = [grade, course, credits, year]


    @staticmethod
    def convertLetterToGrade(letterGrade):
        if letterGrade == "A+" or letterGrade == "A":
            return 4
        elif letterGrade == "A-":
            return 3.7
        elif letterGrade == "B+":
            return 3.3
        elif letterGrade == "B":
            return 3
        elif letterGrade == "B-":
            return 2.7
        elif letterGrade == "C+":
            return 2.3
        elif letterGrade == "C":
            return 2
        elif letterGrade == "C-":
            return 1.7
        elif letterGrade == "D+":
            return 1.3
        elif letterGrade == "D":
            return 1
        elif letterGrade == "D-":
            return 0.7
        elif letterGrade == "F":
            return 0
        else:
            return None

        

    def calculateGPA(self, grades):
        grade_value = 0
        credit = 0
        numOfCredits = 0
        for key, value in grades.items():
            grade_value += Student.convertLetterToGrade(value[0])
            credit += int(value[2])
            numOfCredits += 1
            print("Grade value {}, credits {}".format(grade_value, credit))
        gpa = float(grade_value / numOfCredits)
        self.gpaBySemester.append(gpa)
        return gpa

    def evaluateGPA(self):
        semester_gpa = self.calculateGPA(self.grades)
        overall_gpa = 0

        for i in self.gpaBySemester:
            overall_gpa += i
        self.overallGPA = overall_gpa / len(self.gpaBySemester)

        if semester_gpa >= 2 and semester_gpa <= 2.25:
            self.addWarnings(1)

        if semester_gpa >= 3.75 or self.overallGPA > 3.5:
            self.honorRoll = True
            # Can remove 1 warning if any
            if self.warning > 0:
                self.warning -= 1






    def addWarnings(self, warningCount):
        self.warning += warningCount
        if self.warning >= 3:
            self.suspended = True
            print("Student Will be suspended")


    
    def __repr__(self):
        return '<Student {}, {}>'.format(self.student_id, self.username)


@login.user_loader
def load_user(user):
    return User.get(user)



# Dummy Data

registered_users_table = [
    User("susan", 'cat'), # Registrars
    User("john", 'dog'), # Instructor
    User("tom",'fish')] # Student

registered_users_complaints = [
    User('susan', 'cat').Complaint('susan', '332')
]






