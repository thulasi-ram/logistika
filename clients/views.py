from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from clients.models import Clients


class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['name', 'website']


class ClientsFeed(LoginRequiredMixin, TemplateView):
    template_name = 'clients/clients.html'

    def get(self, request, *args, **kwargs):
        clients = Clients.objects.all()
        page = request.GET.get('page')
        items_per_page = request.META.get('items_per_page', 10)
        paginator = Paginator(clients, items_per_page)
        try:
            clients = paginator.page(page)
        except PageNotAnInteger:
            clients = paginator.page(1)
        except EmptyPage:
            clients = paginator.page(paginator.num_pages)
        page = clients.number
        return TemplateResponse(request, self.template_name, {'clients': clients})


class CreateClient(LoginRequiredMixin, TemplateView):
    template_name = 'clients/create_clients.html'

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.template_name, context={'form': ClientForm})

    def post(self, request):
        data = request.POST
        form = ClientForm(data=data)
        if form.is_valid():
            form.cleaned_data['created_by'] = request.user
            Clients.objects.create(**form.cleaned_data)
            return TemplateResponse(request, self.template_name, context={'form': ClientForm})
        return TemplateResponse(request, self.template_name, context={'form': form})
