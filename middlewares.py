def check_slash_symbol(*args, **kwargs):
    """Проверяем последний символ в url на наличие косой черты"""
    if not kwargs['url'].endswith('/'):
        kwargs['url'] += '/'
    return kwargs['url']


middlewares = [
    check_slash_symbol,
]
