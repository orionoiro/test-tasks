from django import template
from django.utils.html import format_html
from ..models import Category

register = template.Library()


@register.simple_tag(takes_context='True')
def draw_menu(context, menu_slug):
    request = context['request']
    url = request.build_absolute_uri().split('?')[0]
    query_cursor = request.GET.get('cursor', default=None)
    catgs = Category.objects.filter(parent_menu_id__slug=menu_slug).select_related('parent_category')

    if not catgs:
        return format_html(f'{menu_slug} is absent or empty')

    def parse(catgs):
        parents = {}
        roots = []
        cursor_obj = None

        for elem in catgs:
            if elem.slug == query_cursor:
                cursor_obj = elem
            if not elem.parent_category:
                roots.append(elem)
            elif elem.parent_category not in parents:
                parents[elem.parent_category] = []
                parents[elem.parent_category].append(elem)
            else:
                parents[elem.parent_category].append(elem)
        return parents, sorted(roots, key=lambda x: x.category_name), cursor_obj

    def create_branch(cursor_obj):
        branch = []
        while cursor_obj:
            branch.append(cursor_obj)
            cursor_obj = cursor_obj.parent_category
        return branch

    def check_category(category):
        element_html = f'<a href="{url}?cursor={category.slug}">{category.category_name}</a>'
        if category not in current_branch or category not in parent_catgs:
            element_html = f'<li>{element_html}</li>'
            return element_html
        else:
            for child in parent_catgs[category]:
                element_html += f'<ul>{check_category(child)}</ul>'
            element_html = f'<li>{element_html}</li>'
            return element_html

    def build_html():
        html = ''
        for elem in roots:
            html += check_category(elem)
        return f'<ul>{html}</ul>'

    parent_catgs, roots, concrete_cursor = parse(catgs)
    current_branch = create_branch(concrete_cursor)
    final_html = build_html()

    return format_html(final_html)
