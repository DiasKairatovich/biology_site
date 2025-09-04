from django import template
from django.forms.boundfield import BoundField

register = template.Library()


@register.filter(name='add_class')
def add_class(field, css):
    """Добавляет CSS-класс к полю формы"""
    if not isinstance(field, BoundField):
        return field

    existing_classes = field.field.widget.attrs.get('class', '')
    classes = f'{existing_classes} {css}'.strip()
    attrs = field.field.widget.attrs.copy()
    attrs['class'] = classes
    return field.as_widget(attrs=attrs)


@register.filter(name='add_attr')
def add_attr(field, arg):
    """Добавляет атрибуты к полю формы.
    Пример: {{ field|add_attr:"placeholder=Введите текст rows=5" }}
    """
    if not isinstance(field, BoundField):
        return field

    attrs = field.field.widget.attrs.copy()
    pairs = arg.split()
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            attrs[key] = value
        else:
            attrs[pair] = True
    return field.as_widget(attrs=attrs)


@register.filter(name='add_placeholder')
def add_placeholder(field, text):
    """Добавляет placeholder к полю формы"""
    if not isinstance(field, BoundField):
        return field

    attrs = field.field.widget.attrs.copy()
    attrs['placeholder'] = text
    return field.as_widget(attrs=attrs)


@register.filter(name='get_field')
def get_field(form, field_name):
    """Получает поле формы по имени"""
    return form[field_name]


@register.filter(name='add_index')
def add_index(field, index):
    """Добавляет индекс к имени поля (для formset)"""
    if not isinstance(field, BoundField):
        return field

    # Сохраняем оригинальное имя поля
    original_name = field.field.widget.attrs.get('data-original-name', field.name)
    field.field.widget.attrs['data-original-name'] = original_name

    # Заменяем последнюю часть имени на индекс
    name_parts = original_name.split('-')
    if len(name_parts) > 1:
        name_parts[-1] = index
        new_name = '-'.join(name_parts)
        field.field.widget.attrs['name'] = new_name
        field.field.widget.attrs['id'] = f"id_{new_name}"

    return field

@register.filter
def get_field(form, field_name):
    """Получить поле формы по имени"""
    return form[field_name]
