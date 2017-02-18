from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.template_name, {'profile': True})
