from utils import render


def main_view():
    language_list = [{'name': 'Python'},
                     {'name': 'C++'},
                     {'name': 'Golang'}]
    return '200 OK', render(template_name='index.html', language_list=language_list)


def about_view():
    return '200 OK', render('about.html')
