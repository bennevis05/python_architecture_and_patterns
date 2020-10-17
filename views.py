from utils import render, parsing_data


def main_view(request):
    return '200 OK', render(template_name='index.html')


def about_view(request):
    return '200 OK', render(template_name='about.html')


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
