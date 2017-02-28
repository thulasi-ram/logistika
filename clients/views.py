from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from clients.models import Clients, ClientRequests


class ClientForm(forms.Form):
    email = forms.EmailField()


class ClientsFeed(LoginRequiredMixin, TemplateView):
    template_name = 'clients/clients.html'

    def get(self, request, *args, **kwargs):
        clients = Clients.objects.filter(created_by=request.user)
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


class InviteClient(LoginRequiredMixin, TemplateView):
    template_name = 'clients/invite_clients.html'

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


class ViewClient(LoginRequiredMixin, TemplateView):
    template_name = 'clients/view_client.html'

    def get(self, request, *args, **kwargs):
        client = Clients.objects.filter(id=kwargs.get('client_id')).first()
        return TemplateResponse(request, self.template_name, context={'client': client})

    def post(self, request, client_id):
        client = Clients.objects.get(id=client_id)
        if request.POST.get('delete') == 'true' and client.is_active:
            client.is_active = False
            client.save()
        return TemplateResponse(request, self.template_name, context={'client': client})


class ClientRequestsForm(forms.ModelForm):
    class Meta:
        model = ClientRequests
        fields = '__all__'


class ClientRequestsView(LoginRequiredMixin, TemplateView):
    template_name = 'clients/client_requests.html'

    def get(self, request, *args, **kwargs):
        client_reqs = ClientRequests.objects.filter(user=request.user)
        return TemplateResponse(request, self.template_name, context={'client_requests': client_reqs})

    def post(self, request):
        data = request.POST
        if data.get('cli_req_id'):
            cli_req = ClientRequests.objects.get(id=data['cli_req_id'])
            if 'accept' in data:
                cli_req.status = ClientRequests.ACCEPTED
            if 'reject' in data:
                cli_req.status = ClientRequests.REJECTED
            cli_req.save()
        client_reqs = ClientRequests.objects.filter(user=request.user)
        return TemplateResponse(request, self.template_name, context={'client_requests': client_reqs})
