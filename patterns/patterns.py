from abc import ABCMeta, abstractmethod


class AbstractCategory(metaclass=ABCMeta):
    @abstractmethod
    def get_category_name(self):
        pass


class AbstractCourse(metaclass=ABCMeta):
    @abstractmethod
    def get_course_name(self):
        pass


class Composite(metaclass=ABCMeta):
    @abstractmethod
    def get_total_amount(self):
        pass

    @abstractmethod
    def get_total_price(self):
        pass


class Category(AbstractCategory, Composite):
    def __init__(self, name):
        self.name = name
        self.elements = []

    def get_category_name(self):
        return self.name

    def add(self, element):
        self.elements.append(element)

    def get_total_amount(self):
        total_amount = 0
        for elem in self.elements:
            total_amount += elem.get_total_amount()
        return total_amount

    def get_total_price(self):
        total_price = 0
        for elem in self.elements:
            total_price += elem.get_total_price()
        return total_price


class Course(AbstractCourse, Composite):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.price = 10000

    def get_course_name(self):
        return self.name

    def get_total_amount(self):
        return 1

    def get_total_price(self):
        return self.price


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
