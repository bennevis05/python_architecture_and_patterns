import os
from jinja2 import Template


def render(template_name, template_folder='templates', **kwargs):
    """Функция рендера шаблона"""
    template_path = os.path.join(template_folder, template_name)

    with open(template_path, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)
