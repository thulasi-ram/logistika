from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView


class Logout(TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        referrer = request.build_absolute_uri(reverse('landing'))
        if request.user:
            logout(request)
        return HttpResponseRedirect(referrer)