from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import TemplateView

from organizations.models import OrganizationRequests, Organization


class UserOrganization(LoginRequiredMixin, TemplateView):
    template_name = 'users/organization.html'

    def get(self, request, *args, **kwargs):
        try:
            org_req = OrganizationRequests.objects.filter(user=request.user).latest('created_at')
        except OrganizationRequests.DoesNotExist:
            org_req = None
        return TemplateResponse(request, self.template_name, context={'org_req': org_req})

    def post(self, request):
        data = request.POST
        if data.get('organization'):
            org = Organization.objects.get(name=data['organization'])
            org.org_req.create(user=request.user)
        return HttpResponseRedirect(reverse('users:organization'))