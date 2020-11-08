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
