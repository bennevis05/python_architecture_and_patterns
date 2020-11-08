from patterns.patterns import AbstractCategory, AbstractCourse, AbstractUser,\
    Composite, Subject, Observer

import sqlite3
import threading


connection = sqlite3.connect('portal_database.sqlite')


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.update_objects = []
        self.removed_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_update(self, obj):
        self.update_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.create_new()
        self.update_object()
        self.remove_object()

    def create_new(self):
        for obj in self.new_objects:
            MapperRegistry.get_mapper(obj).create(obj)

    def update_object(self):
        for obj in self.update_objects:
            MapperRegistry.get_mapper(obj).update(obj)

    def remove_object(self):
        for obj in self.removed_objects:
            MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DatabaseObject:
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_update(self):
        UnitOfWork.get_current().register_update(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


class CategoryMapper:
    def __init__(self, connect):
        self.connection = connect
        self.cursor = connect.cursor()

    def create(self, category):
        sql_statement = "INSERT INTO categories (name) VALUES (?)"
        self.cursor.execute(sql_statement, (category.name,))
        self.connection.commit()

    def read(self):
        sql_statement = "SELECT * FROM categories"
        self.cursor.execute(sql_statement)
        return [LearningPortal.create_category(*category) for category
                in self.cursor.fetchall()]


class CourseMapper:
    def __init__(self, connect):
        self.connection = connect
        self.cursor = connect.cursor()

    def create(self, course):
        sql_statement = """INSERT INTO courses VALUES (?, ?, ?, ?)"""
        self.cursor.execute(sql_statement, (course.name, course.category,
                                            course.price, course.course_type))
        self.connection.commit()

    def read(self):
        sql_statement = "SELECT * FROM courses"
        self.cursor.execute(sql_statement)
        return [LearningPortal.create_course(*course) for course
                in self.cursor.fetchall()]


class UserMapper:
    def __init__(self, connect):
        self.connection = connect
        self.cursor = connect.cursor()

    def create(self, user):
        sql_statement = """INSERT INTO users VALUES (?, ?, ?, ?, ?)"""
        self.cursor.execute(sql_statement, (user.name, user.surname, user.email,
                                            user.city, user.state))
        self.connection.commit()


class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Category):
            return CategoryMapper(connection)
        elif isinstance(obj, Course):
            return CourseMapper(connection)
        elif isinstance(obj, User):
            return UserMapper(connection)


class Category(AbstractCategory, Composite, DatabaseObject):
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


class Course(AbstractCourse, Composite, Subject, DatabaseObject):
    def __init__(self, name, category, price=10000):
        self.name = name
        self.category = category
        self.price = price
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
    def __init__(self, name, category, price, course_type):
        super().__init__(name, category, price)
        self.course_type = course_type


class OfflineCourse(Course):
    def __init__(self, name, category, price, course_type):
        super().__init__(name, category, price)
        self.course_type = course_type


class User(AbstractUser, Observer, DatabaseObject):
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


class CourseFactory:
    course_type = {
        'Online': OnlineCourse,
        'Offline': OfflineCourse
    }

    @classmethod
    def create_course(cls, name, category, price, type_course):
        return cls.course_type[type_course](name, category, price, type_course)


class LearningPortal:
    def __init__(self):
        self.all_categories = []
        self.all_courses = []
        self.all_students = []

    @staticmethod
    def create_category(name):
        return Category(name)

    @staticmethod
    def create_course(name, category, price, course_type):
        return CourseFactory.create_course(name, category, price, course_type)

    @staticmethod
    def create_user(name, surname, email, city, state):
        return User(name, surname, email, city, state)

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
