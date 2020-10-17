from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment


def render(template_name, templates_folder='templates', **kwargs):
    """Функция рендера шаблона"""

    env = Environment()
    env.loader = FileSystemLoader(templates_folder)
    template = env.get_template(template_name)

    return template.render(**kwargs)


def parsing_data(data):
    """Парсинг данных"""
    result = {}
    if data:
        for item in data.split('&'):
            key, value = item.split('=')
            result[key] = value
    return result
