from abc import ABCMeta, abstractmethod


class AbstractCategory(metaclass=ABCMeta):
    @abstractmethod
    def get_category_name(self):
        pass

    @abstractmethod
    def get_number_of_courses(self):
        pass


class AbstractCourse(metaclass=ABCMeta):
    pass


class Category(AbstractCategory):
    def __init__(self, name):
        self.name = name
        self.courses = []

    def get_category_name(self):
        return self.name

    def get_number_of_courses(self):
        return len(self.courses)


class Course(AbstractCourse):
    def __init__(self, name, category):
        self.name = name
        self.category = category


class OnlineCourse(Course):
    def __init__(self, name, category, course_type):
        super().__init__(name, category)
        self.course_type = course_type


class OfflineCourse(Course):
    def __init__(self, name, category, course_type):
        super().__init__(name, category)
        self.course_type = course_type


class CourseFactory:
    course_type = {
        'Online': OnlineCourse,
        'Offline': OfflineCourse
    }

    @classmethod
    def create_course(cls, name, category, type_course):
        return cls.course_type[type_course](name, category, type_course)
