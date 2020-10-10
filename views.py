from utils import render, parsing_data


def main_view(request):
    language_list = [{'name': 'Python'},
                     {'name': 'C++'},
                     {'name': 'Golang'}]
    return '200 OK', render(template_name='index.html', language_list=language_list)


def about_view(request):
    return '200 OK', render(template_name='about.html')


def contact_view(request):
    if request['REQUEST_METHOD'] == 'POST':
        data = request['wsgi.input'].read().decode(encoding='utf-8')
        print('Метод передачи данных "POST"')
        print('Данные:', parsing_data(data))
    else:
        data = request['QUERY_STRING']
        print('Метод передачи данных "GET"')
        print('Данные:', parsing_data(data))

    return '200 OK', render(template_name='contact.html',)
