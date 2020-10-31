from abc import ABCMeta, abstractmethod


class AbstractCategory(metaclass=ABCMeta):
    @abstractmethod
    def get_category_name(self):
        pass


class AbstractCourse(metaclass=ABCMeta):
    @abstractmethod
    def get_course_name(self):
        pass


class AbstractUser(metaclass=ABCMeta):
    @abstractmethod
    def full_name(self):
        pass


class Composite(metaclass=ABCMeta):
    @abstractmethod
    def get_total_amount(self):
        pass

    @abstractmethod
    def get_total_price(self):
        pass


class Subject(metaclass=ABCMeta):
    @abstractmethod
    def attach(self, observer):
        pass

    @abstractmethod
    def detach(self, observer):
        pass

    @abstractmethod
    def notify(self):
        pass


class Observer(metaclass=ABCMeta):
    @abstractmethod
    def send_notification(self, course):
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


class Course(AbstractCourse, Composite, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.price = 10000
        self.course_type = None
        self.all_observers = []

    def get_course_name(self):
        return self.name

    def get_total_amount(self):
        return 1

    def get_total_price(self):
        return self.price

    def set_name(self, new_name):
        self.name = new_name

    def set_category(self, new_category):
        self.category = new_category

    def set_price(self, new_price):
        self.price = new_price

    def set_type(self, new_type):
        self.course_type = new_type

    def attach(self, observer):
        self.all_observers.append(observer)

    def detach(self, observer):
        self.all_observers.remove(observer)

    def notify(self):
        for observer in self.all_observers:
            observer.send_notification(self)


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


class Student(AbstractUser, Observer):
    def __init__(self, name, surname, email, city, state):
        self.name = name
        self.surname = surname
        self.email = email
        self.city = city
        self.state = state
        self.course_list = []

    def full_name(self):
        return f'{self.name} {self.surname}'

    def send_notification(self, course):
        print(f'Добрый день, {self.full_name()}! '
              f'На одном из ваших курсов произошли изменения:')
        print(f'{course.name}\n{course.category}\n{course.price}\n'
              f'{course.course_type}')
