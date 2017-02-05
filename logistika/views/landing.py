from django.template.response import TemplateResponse
from django.views.generic import TemplateView


class Landing(TemplateView):
    template_name = 'logistika/landing.html'

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.template_name)