from django import template


register = template.Library()


@register.filter
def capitalize(value):
    return value.capitalize()


@register.filter
def shrink(value):
    if len(value) < 140:
        return value
    return value[:139]


@register.filter
def get_index(item, lst):
    return lst.index(item)


@register.filter
def multiply(value):
    value = int(value)
    return str(value * 100)


@register.filter
def alphabet(value):
    if int(value) == 1:
        return 'a'
    elif int(value) == 2:
        return 'b'
    elif int(value) == 3:
        return 'c'
    elif int(value) == 4:
        return 'd'
    elif int(value) == 5:
        return 'e'


@register.filter
def string(value):
    return str(value)


@register.filter
def is_int(value):
    return type(value) == int


@register.filter
def calculate(results, language):
    scores = []
    count = language.stage_set.count()
    for result in results:
        if result.study_material.stage.language == language:
            scores.append(result.score)
    progress = 0
    if count != 0:
        progress = sum(scores) / count
    return progress

