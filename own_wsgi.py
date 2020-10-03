from jinja2 import Template


class Response:
    def __init__(self, code, body):
        self.code = code
        self.body = body


class Views:
    @staticmethod
    def main_view(template_name, legal_info='', **kwargs):
        with open(template_name, encoding='utf-8') as f:
            template = Template(f.read())
            template_render = f'{template.render(**kwargs)}{legal_info}'.encode(encoding='utf-8')
        return Response('200 OK', [template_render])

    @staticmethod
    def about_view(legal_info=''):
        body = f'<h1>About Page</h1>{legal_info}'.encode(encoding='utf-8')
        return Response('200 OK', [body])


class Application:
    def __init__(self, urls, middlewares):
        self.urls = urls
        self.middlewares = middlewares

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """
        url = environ['PATH_INFO']
        # Проверка на символ слеш в конце адреса
        if url[-1] != '/':
            url += '/'

        view = self.urls[url]
        additional_content = None

        for elem in self.middlewares:
            additional_content = elem()

        if url == '/':
            response = view('index.html', additional_content, language_list=[{'name': 'Python'},
                                                                             {'name': 'C++'},
                                                                             {'name': 'Golang'}])
        else:
            response = view(additional_content)
        start_response(response.code, [('Content-Type', 'text/html')])
        return response.body


def legal_info_middleware():
    """Добавляем на страницу информацию о правах"""
    return '<hr><p>&laquo;SM&raquo; &copy; &laquo;All rights reserved&raquo;</p>'


views = Views()

urls = {
    '/': views.main_view,
    '/about/': views.about_view
}

middlewares = [
    legal_info_middleware,
]

application = Application(urls, middlewares)
