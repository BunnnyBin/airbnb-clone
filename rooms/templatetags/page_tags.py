#커스텀 템플릿 태그
from django import template

register = template.Library()

@register.filter(name="next_page") # name : 함수 이름과 다른데 호출할 때 쓰는 이름
def next_page(value): # value : filter가 적용되는 값
    split = value.split("&")
    for s in split:
        if "page=" in s:
            page_num = str(int(s.replace("page=", "")) + 1)
            value = value.replace(s, "page=" + page_num)
    return value


@register.filter(name="previous_page")
def previous_page(value):
    split = value.split("&")
    for s in split:
        if "page=" in s:
            page_num = str(int(s.replace("page=", "")) - 1)
            value = value.replace(s, "page=" + page_num)
    return value