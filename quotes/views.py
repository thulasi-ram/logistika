from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import serializers
from rest_framework.views import APIView

from quotes.models import Quotes


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

class CreateQuote(TemplateView):
    template_name = 'quotes/quotes.html'
    serializer = QuoteSerializer

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('quotes:consolidated'))

    def post(self, request):
        try:
            data = request.POST
            serializer = self.serializer(data=data)
            if serializer.is_valid():
                quote = Quotes.objects.create(title=serializer.data['title'])
            return TemplateResponse(request, self.template_name)
        except Exception as e:
            return TemplateResponse(request, self.template_name)



