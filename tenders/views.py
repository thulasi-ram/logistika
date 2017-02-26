from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from audit.models import TendersAudit
from quotes.models import Quotes
from tenders import signals
from tenders.models import Tenders


class TenderForm(forms.ModelForm):
    class Meta:
        model = Tenders
        fields = ['title', 'description']


class TendersFeed(TemplateView):
    template_name = 'tenders/tenders.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('q') == 'my' and request.user.is_authenticated:
            tenders = Tenders.objects.filter(created_by=request.user)
        else:
            tenders = Tenders.objects.filter(is_active=True)
        page = request.GET.get('page')
        items_per_page = request.META.get('items_per_page', 10)
        paginator = Paginator(tenders, items_per_page)
        try:
            tenders = paginator.page(page)
        except PageNotAnInteger:
            tenders = paginator.page(1)
        except EmptyPage:
            tenders = paginator.page(paginator.num_pages)
        page = tenders.number
        return TemplateResponse(request, self.template_name, {'tenders': tenders})


class CreateTender(LoginRequiredMixin, TemplateView):
    template_name = 'tenders/create_tender.html'

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.template_name, context={'form': TenderForm})

    def post(self, request):
        data = request.POST
        form = TenderForm(data=data)
        if form.is_valid():
            form.cleaned_data['created_by'] = request.user
            tender = Tenders.objects.create(**form.cleaned_data)
            signals.tender_created.send(sender=Tenders, instance=tender, user=request.user)
            return TemplateResponse(request, self.template_name, context={'form': TenderForm})
        return TemplateResponse(request, self.template_name, context={'form': form})


class ViewTender(LoginRequiredMixin, TemplateView):
    template_name = 'tenders/view_tender.html'

    def get(self, request, *args, **kwargs):
        tender = Tenders.objects.filter(id=kwargs.get('tender_id')).first()
        quotes = Quotes.objects.filter(tender=tender,is_active=True)
        return TemplateResponse(request, self.template_name, context={'tender': tender, 'quotes': quotes})

    def post(self, request, tender_id):
        tender = Tenders.objects.get(id=tender_id)
        quotes = Quotes.objects.filter(tender=tender, is_active=True)
        if request.POST.get('delete') == 'true' and tender.is_active:
            tender.is_active = False
            tender.save()
            signals.tender_deleted.send(sender=Tenders, instance=tender, user=request.user)
        return TemplateResponse(request, self.template_name, context={'tender': tender, 'quotes': quotes})