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

        for middleware in self.middlewares:
            url = middleware(url=url)

        if url in self.urls:
            view = self.urls[url]

            code_response, body_response = view()
            start_response(code_response, [('Content-Type', 'text/html')])
            return [body_response.encode('utf-8')]
        else:
            start_response('404 Not Found', [('Content-Type', 'text/html')])
            return [b"PAGE NOT FOUND"]
