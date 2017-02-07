from django.core.serializers.json import Serializer

class QuotesJSONSerializer(Serializer):

    def get_dump_object(self, obj):
        return self._current