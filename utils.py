import os
from jinja2 import Template


def render(template_name, template_folder='templates', **kwargs):
    """Функция рендера шаблона"""
    template_path = os.path.join(template_folder, template_name)

    with open(template_path, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)


def parsing_data(data):
    """Парсинг данных"""
    result = {}
    if data:
        for item in data.split('&'):
            key, value = item.split('=')
            result[key] = value
    return result
