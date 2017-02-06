from django.template.response import TemplateResponse
from django.views.generic import TemplateView


class Profile(TemplateView):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        # data = request.user.profile_data()
        data = {}
        return TemplateResponse(request, self.template_name, {'profile': True})