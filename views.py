from utils import render, parsing_data, debug
from models import LearningPortal

from urllib.parse import unquote
import json


portal = LearningPortal()


@debug
def main_view(request):
    return '200 OK', render(template_name='index.html')


def categories_view(request):
    page_content = {
        'all_categories': portal.all_categories
    }
    return '200 OK', render(**page_content, template_name='categories.html')


def add_category_view(request):
    if request['REQUEST_METHOD'] == 'POST':
        content_length = int(request.get('CONTENT_LENGTH'))
        data = parsing_data(unquote(request['wsgi.input'].read(content_length).
                                    decode(encoding='utf-8')))

        category_name = data['category_name']
        sup_category_name = data['sup_category_name']

        if sup_category_name == 'Выберите подкатегорию':
            new_category = portal.create_category(category_name)
            portal.all_categories.append(new_category)
        else:
            new_category = portal.create_category(category_name)
            portal.all_categories.append(new_category)
            portal.get_category(sup_category_name).add(new_category)

        page_content = {
            'all_categories': portal.all_categories,
            'all_courses': portal.all_courses
        }
        return '200 OK', render(**page_content, template_name='manage_page.html')
    else:
        page_content = {
            'all_categories': portal.all_categories,
            'all_courses': portal.all_courses
        }
        return '200 OK', render(**page_content, template_name='manage_page.html')


def courses_view(request):
    return '200 OK', render(template_name='courses.html',
                            all_courses=portal.all_courses)


def add_course_view(request):
    if request['REQUEST_METHOD'] == 'POST':
        content_length = int(request.get('CONTENT_LENGTH'))
        data = parsing_data(unquote(request['wsgi.input'].read(content_length).
                                    decode(encoding='utf-8')))

        course_name = data['course_name']
        category_name = data['category_name']
        course_format = data['course_format']

        new_course = portal.create_course(course_name, category_name,
                                          course_format)
        portal.all_courses.append(new_course)
        portal.get_category(category_name).add(new_course)

        page_content = {
            'all_categories': portal.all_categories,
            'all_courses': portal.all_courses
        }
        return '200 OK', render(**page_content, template_name='manage_page.html')
    else:
        page_content = {
            'all_categories': portal.all_categories,
            'all_courses': portal.all_courses
        }
        return '200 OK', render(**page_content, template_name='manage_page.html')


def add_user_view(request):
    if request['REQUEST_METHOD'] == 'POST':
        content_length = int(request.get('CONTENT_LENGTH'))
        data = parsing_data(unquote(request['wsgi.input'].read(content_length).
                                    decode(encoding='utf-8')))

        user_name = data['user_name']
        user_surname = data['user_surname']
        user_email = data['user_email']
        user_city = data['user_city']
        user_state = data['user_state']
        user_course_name = data['user_course']

        new_user = portal.create_user(user_name, user_surname, user_email,
                                      user_city, user_state)
        user_course = portal.get_course(user_course_name)
        new_user.course_list.append(user_course)
        user_course.attach(new_user)

        portal.all_students.append(new_user)

        for student in portal.all_students:
            print(student.full_name())
            for course in student.course_list:
                print(f'----{course.get_course_name()}')

        page_content = {
            'all_categories': portal.all_categories,
            'all_courses': portal.all_courses
        }
        return '200 OK', render(**page_content, template_name='manage_page.html')
    else:
        page_content = {
            'all_categories': portal.all_categories,
            'all_courses': portal.all_courses
        }
        return '200 OK', render(**page_content, template_name='manage_page.html')


def contact_view(request):
    if request['REQUEST_METHOD'] == 'POST':
        content_length = int(request.get('CONTENT_LENGTH'))
        data = request['wsgi.input'].read(content_length).decode(encoding=
                                                                 'utf-8')
        print('Метод передачи данных "POST"')
        print('Данные:', parsing_data(data))
    else:
        data = request['QUERY_STRING']
        print('Метод передачи данных "GET"')
        print('Данные:', parsing_data(data))

    return '200 OK', render(template_name='contact.html',)


def manage_page_view(request):
    page_content = {
        'all_categories': portal.all_categories,
        'all_courses': portal.all_courses
    }
    return '200 OK', render(**page_content, template_name='manage_page.html')


def change_course(request):
    if request['REQUEST_METHOD'] == 'POST':
        content_length = int(request.get('CONTENT_LENGTH'))
        data = parsing_data(unquote(request['wsgi.input'].read(content_length).
                                    decode(encoding='utf-8')))

        course_name = data['course_name']
        course_to_change = portal.get_course(course_name)

        page_content = {
            'all_categories': portal.all_categories,
            'course_to_change': course_to_change
        }
        return '200 OK', render(**page_content,
                                template_name='change_course.html')
    else:
        page_content = {
            'all_categories': portal.all_categories,
            'all_courses': portal.all_courses
        }
        return '200 OK', render(**page_content, template_name='manage_page.html')


def change_course_confirm(request):
    if request['REQUEST_METHOD'] == 'POST':
        content_length = int(request.get('CONTENT_LENGTH'))
        data = parsing_data(unquote(request['wsgi.input'].read(content_length).
                                    decode(encoding='utf-8')))

        course_to_change = portal.get_course(data['course_name'])

        course_new_name = data['course_new_name']
        if course_new_name:
            course_to_change.set_name(course_new_name)

        category_name = data['category_name']
        if category_name != 'Выберите категорию':
            course_to_change.set_category(category_name)

        course_price = data['course_price']
        if course_price:
            course_to_change.set_price(course_price)

        course_format = data['course_format']
        if course_format != 'Выберите формат':
            course_to_change.set_type(course_format)

        course_to_change.notify()

        page_content = {
            'all_categories': portal.all_categories,
            'all_courses': portal.all_courses
        }
        return '200 OK', render(**page_content,
                                template_name='manage_page.html')
    else:
        page_content = {
            'all_categories': portal.all_categories,
            'all_courses': portal.all_courses
        }
        return '200 OK', render(**page_content,
                                template_name='manage_page.html')


def api_get_courses(request):
    all_courses = json.dumps([course.__dict__ for course in portal.all_courses],
                             sort_keys=True, indent=4)
    print(all_courses)
    return all_courses


def test_api(request):
    with open('courses.json', 'w') as f:
        json.dump(api_get_courses(request), f)
    return '200 OK', render(template_name='index.html')
