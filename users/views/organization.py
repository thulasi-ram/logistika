from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.views.generic import TemplateView


class UserOrganization(LoginRequiredMixin, TemplateView):
    template_name = 'users/organization.html'

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.template_name)