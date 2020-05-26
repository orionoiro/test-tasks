from rest_framework import serializers
from .models import Record


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        exclude = ('id',)
        read_only_fields = ('category', 'sender', 'title', 'text', 'greeting_id')

    def to_representation(self, instance):
        original = super(RecordSerializer, self).to_representation(instance)
        renamed = {'category': original['category'],
                   'from': original['sender'],
                   'title': original['title'],
                   'text': original['text'],
                   'thedate': original['date'],
                   'id': original['greeting_id']
                   }
        return renamed
