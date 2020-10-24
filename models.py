from patterns.patterns import Category, CourseFactory


class LearningPortal:
    def __init__(self):
        self.all_categories = []
        self.all_courses = []

    @staticmethod
    def create_category(name):
        return Category(name)

    @staticmethod
    def create_course(name, category, course_type):
        return CourseFactory.create_course(name, category, course_type)
