from patterns.patterns import Category, CourseFactory, Student


class LearningPortal:
    def __init__(self):
        self.all_categories = []
        self.all_courses = []
        self.all_students = []

    @staticmethod
    def create_category(name):
        return Category(name)

    @staticmethod
    def create_course(name, category, course_type):
        return CourseFactory.create_course(name, category, course_type)

    @staticmethod
    def create_user(name, surname, email, city, state):
        return Student(name, surname, email, city, state)

    def get_category(self, name):
        for elem in self.all_categories:
            if name == elem.get_category_name():
                return elem
        return None

    def get_course(self, name):
        for elem in self.all_courses:
            if name == elem.get_course_name():
                return elem
        return None
