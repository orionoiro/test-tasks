from django.contrib import admin
from django import forms
from .models import Menu, Category


class MenuItemInLine(admin.TabularInline):
    model = Category
    exclude = ('slug', )


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('slug', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent_category'].queryset = self.fields['parent_category'].queryset.exclude(pk=self.instance.pk)


@admin.register(Category)
class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemForm

    list_display = (
        'category_name',
        'parent_menu',
        'parent_category')
    exclude = ('slug', )


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('menu_name',)
    exclude = ('slug', )
    inlines = (MenuItemInLine, )