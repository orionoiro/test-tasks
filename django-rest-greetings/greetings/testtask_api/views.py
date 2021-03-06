import datetime
from rest_framework import mixins, generics
from drf_renderer_xlsx.mixins import XLSXFileMixin
from .models import Record
from .serializers import RecordSerializer


class RecordsView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  XLSXFileMixin,
                  generics.GenericAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filename = 'greetings.xlsx'

    def get_queryset(self):
        date = self.request.query_params.get('date', None)
        if date:
            self.queryset = Record.objects.filter(date=datetime.date.fromisoformat(date))
        return self.queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # HTML-form browsable-api date filtering

        if request.data['date']:
            date = request.data['date']
            self.queryset = Record.objects.filter(date=datetime.date.fromisoformat(date))
        return self.list(request, *args, **kwargs)
