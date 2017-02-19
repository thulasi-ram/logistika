from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from quotes.models import Quotes
from tenders.models import Tenders


class QuotesFeed(LoginRequiredMixin, TemplateView):
    template_name = 'quotes/quotes.html'

    def get(self, request, *args, **kwargs):
        quotes = Quotes.objects.filter(created_by=request.user)
        page = request.GET.get('page')
        items_per_page = request.META.get('items_per_page', 10)
        paginator = Paginator(quotes, items_per_page)
        try:
            quotes = paginator.page(page)
        except PageNotAnInteger:
            quotes = paginator.page(1)
        except EmptyPage:
            quotes = paginator.page(paginator.num_pages)
        page = quotes.number
        return TemplateResponse(request, self.template_name, {'quotes': quotes})

class QuotesForm(forms.ModelForm):
    class Meta:
        model = Quotes
        fields = ['title', 'description']

class CreateQuote(LoginRequiredMixin, TemplateView):
    template_name = 'quotes/create_quotes.html'

    def get(self, request, *args, **kwargs):
        tender = request.GET.get('tender')
        return TemplateResponse(request, self.template_name, context={'form': QuotesForm, 'tender': tender})

    def post(self, request):
        data = request.POST
        form = QuotesForm(data=data)
        if form.is_valid():
            form.cleaned_data['created_by'] = request.user
            form.cleaned_data['tender'] = Tenders.objects.get(id=data.get('tender'))
            Quotes.objects.create(**form.cleaned_data)
            return TemplateResponse(request, self.template_name, context={'form': QuotesForm})
        return TemplateResponse(request, self.template_name, context={'form': form})


class ViewQuote(LoginRequiredMixin, TemplateView):
    template_name = 'quotes/view_quote.html'

    def get(self, request, *args, **kwargs):
        quote = Quotes.objects.filter(id=kwargs.get('quote_id')).first()
        return TemplateResponse(request, self.template_name, context={'quote': quote})

    def post(self, request, quote_id):
        quote = Quotes.objects.get(id=quote_id)
        if request.POST.get('delete') == 'true' and quote.is_active:
            quote.is_active = False
            quote.save()
        return TemplateResponse(request, self.template_name, context={'quote': quote})