from django.core import serializers as dj_serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers.python import  Serializer as BaseSerializer
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import traceback
from quotes.models import Quotes
from quotes.serializers import QuotesJSONSerializer


class QuotesConsolidated(TemplateView):
    template_name = 'quotes/quotes.html'

    def get(self, request, *args, **kwargs):
        quotes = Quotes.objects.all()
        return TemplateResponse(request, self.template_name, {'quotes': quotes})

class QuoteSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, error_messages={
        'required': 'Quote title is required',
        'blank': 'Quote title cannot be blank'
    })

class ListQuotes(APIView):

    def get(self, request):
        try:
            quotes = Quotes.objects.all()
            page = request.GET.get('page')
            items_per_page = request.META.get('items_per_page', 10)
            paginator = Paginator(quotes, items_per_page)
            try:
                quotes = paginator.page(page)
            except PageNotAnInteger:
                quotes = paginator.page(1)
            except EmptyPage:
                quotes = paginator.page(paginator.num_pages)
            serializer = QuotesJSONSerializer()
            page = quotes.number
            quotes = serializer.serialize(quotes, fields=('title'))
            return Response(data={'quotes': quotes, 'total_pages': paginator.num_pages, 'curr_page': page, 'items_per_page': items_per_page}, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response("Quote listing failed.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateQuote(APIView):
    serializer = QuoteSerializer
    authentication_classes = []

    def post(self, request):
        try:
            data = request.POST
            serializer = self.serializer(data=data)
            if serializer.is_valid():
                Quotes.objects.create(title=serializer.data['title'])
            return Response("Quote created", status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Quote creation failed.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)



