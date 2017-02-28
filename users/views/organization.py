from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from organizations.models import OrganizationRequests


class UserOrganization(LoginRequiredMixin, TemplateView):
    template_name = 'users/organization.html'

    def get(self, request, *args, **kwargs):
        try:
            org_req = OrganizationRequests.objects.get(user=request.user)
        except OrganizationRequests.DoesNotExist:
            org_req = None
        return TemplateResponse(request, self.template_name, context={'org_req': org_req})