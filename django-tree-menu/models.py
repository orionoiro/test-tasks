from itertools import count

from django.db import models
from django.template.defaultfilters import slugify

max_slug_length = 70

class Menu(models.Model):
    menu_name = models.CharField(max_length=70, default='', verbose_name='Menu name')
    slug = models.SlugField()
    def __str__(self):
        return self.menu_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.menu_name)[:max_slug_length]
        for x in count(1):
            if not Menu.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                break
            self.slug = "%s-%d" % (self.slug[:max_slug_length - len(str(x)) - 1], x)
        super(Menu, self).save(*args, **kwargs)


class Category(models.Model):

    category_name = models.CharField(max_length=70, default='', verbose_name='Category name')
    parent_menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField()


    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)[:max_slug_length]
        for x in count(1):
            if not Category.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                break
            self.slug = "%s-%d" % (self.slug[:max_slug_length - len(str(x)) - 1], x)
        super(Category, self).save(*args, **kwargs)