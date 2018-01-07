from django import template

register = template.Library()


@register.filter(name='list_index')
def list_index(a, b):
    return a[b]


@register.filter(name='inc')
def inc(a, step):
    c = str(int(a) + int(step))
    return c


@register.filter(name='rank_score')
def rank_score(indexed_list, url):
    return float("{0:.5f}".format(indexed_list[url]))
