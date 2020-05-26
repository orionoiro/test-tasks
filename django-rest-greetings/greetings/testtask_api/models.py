from django.db import models


class Record(models.Model):
    category = models.CharField(max_length=100, blank=False, verbose_name='Category')
    sender = models.CharField(max_length=100, blank=False, db_column='from', verbose_name='From')
    title = models.CharField(max_length=100, blank=False, verbose_name='Title')
    text = models.TextField(blank=False, verbose_name='Text')
    date = models.DateField(blank=False, db_column='Date', verbose_name='Date')
    greeting_id = models.IntegerField(blank=False, verbose_name='id')

    class Meta:
        verbose_name_plural = 'records'

    def __str__(self):
        return f'{self.category} from {self.sender}'
