from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from organizations.models import Organization


class OrganizationView(LoginRequiredMixin, TemplateView):
    template_name = 'organizations/organization.html'

    def get(self, request, *args, **kwargs):
        try:
            org = Organization.objects.get(id=kwargs['org_name'])
            return TemplateResponse(request, self.template_name, {'org': org})
        except Organization.DoesNotExist:
            raise Http404('Organization does not exist.')
        except KeyError:
            raise Http404('Organization not given')
