from utils import render, parsing_data, debug
from models import LearningPortal

from urllib.parse import unquote


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
            'all_categories': portal.all_categories
        }
        return '200 OK', render(**page_content, template_name='manage_page.html')
    else:
        return '200 OK', render(template_name='manage_page.html')


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

        return '200 OK', render(template_name='manage_page.html',
                                all_categories=portal.all_categories,
                                all_courses=portal.all_courses)
    else:
        return '200 OK', render(template_name='manage_page.html')


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
    return '200 OK', render(template_name='manage_page.html',
                            all_categories=portal.all_categories)
