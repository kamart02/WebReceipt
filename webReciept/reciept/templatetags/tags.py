from django import template

register = template.Library()

@register.filter(name = 'removeUserAndCutTo4')
def removeUserAndCutTo4(querryset, user):
    return querryset.exclude(id = user.id)[:4]

@register.filter(name = 'removeUser')
def removeUser(querryset, user):
    return querryset.exclude(id = user.id)

@register.filter(name = 'cutZeros')
def cutZeros(number):
    return str(number).rstrip('0').rstrip('.')

