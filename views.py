from utils import render, parsing_data
from models import LearningPortal

from urllib.parse import unquote

portal = LearningPortal()


def main_view(request):
    return '200 OK', render(template_name='index.html')


def categories(request):
    if request['REQUEST_METHOD'] == 'POST':
        content_length = int(request.get('CONTENT_LENGTH'))
        data = unquote(request['wsgi.input'].read(content_length).
                       decode(encoding='utf-8'))
        category_name = data.split('=')[1]

        new_category = portal.create_category(category_name)
        portal.all_categories.append(new_category)

        return '200 OK', render(template_name='categories.html',
                                all_categories=portal.all_categories)
    else:
        return '200 OK', render(template_name='categories.html',
                                all_categories=portal.all_categories)


def courses(request):
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

        return '200 OK', render(template_name='courses.html',
                                all_categories=portal.all_categories,
                                all_courses=portal.all_courses)
    else:
        return '200 OK', render(template_name='courses.html',
                                all_categories=portal.all_categories,
                                all_courses=portal.all_courses)


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
