
#### load the data with fixtures

url patterns:
>
>/records.json
>
>/records.xlsx
>
enabling filtering by date
>
>/records.json?date=<ISO FORMAT>
>
>/records.xlsx?date=<ISO FORMAT>
>
>/records.json?date=2013-07-26
>
>/records.xlsx?date=2013-07-26


rest settings:
>
>REST_FRAMEWORK = {
>    'DEFAULT_RENDERER_CLASSES': [
>        'rest_framework.renderers.JSONRenderer',
>        'rest_framework.renderers.BrowsableAPIRenderer',
>        'drf_renderer_xlsx.renderers.XLSXRenderer',
>    ],
>    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
>    'PAGE_SIZE': 10,
>
>}
