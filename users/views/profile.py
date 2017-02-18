from string import Template

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import widgets, ClearableFileInput


class PictureWidget(widgets.Widget):
    def render(self, name, value, attrs=None):
        html = Template("""<img src="$link"/>""")
        return mark_safe(html.substitute(link=value))

class MLPW(widgets.MultiWidget):
    def __init__(self):
        _widgets = [ClearableFileInput, PictureWidget]
        super(MLPW, self).__init__(_widgets)

    def decompress(self, value):
        if value:
            return [value.day, value.month, value.year]
        return [None, None, None]

class ProfileForm(forms.Form):
    image = forms.ImageField(label='Change profile pic', widget=MLPW)
    name = forms.CharField()
    email = forms.EmailField()

class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.template_name, {'form': ProfileForm})

    def post(self, request):
        return None
