class Students():
    """This is a step towards modelling a class of students"""
    def __init__(self, name, subject, score):
        """Beginning with name, subject and score attributes"""
        self.name = name
        self.subject = subject
        self.score = score
    def fetch_students_details(self):
        """Aim is to retrieve student's name, subject and score"""
        full_details = self.name.title() + " scored a total of " + str(self.score) + " in " + self.subject.title() + "."
        return full_details

class National_details():
    """For describing the details of the student's nationality, including their sponsorship"""
    def __init__(self, nationality = "European"):
        """This initiates the student's national attributes"""
        self.nationality = nationality
    def describe_national_details(self):
        """Produce a message about each student's nationality"""
        print("This student's nationality is " + self.nationality + ".")
    def get_scholarship(self):
        """Print a message about the student's scholarship"""
        if self.nationality == "European":
            scholarship = "full"
        elif self.nationality != "European":
            scholarship = "nil"
        statement = "This student is on " + scholarship + " scholarship"
        print(statement)
        
class Foreign_students(Students):
    """For students who come from other countries"""
    def __init__(self, name, subject, score):
        """This is to begin with the attributes of the parent class"""
        """It is also to create attributes of the child class"""
        super().__init__(name, subject, score)
        self.national_details = National_details()
