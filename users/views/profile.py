from string import Template

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import widgets, ClearableFileInput, TextInput
from rest_framework import serializers

from users.models import Profile


class ProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100,
                                       required=False,
                                       error_messages={
                                           'required': 'First name is required',
                                           'blank': 'First name cannot be blank',
                                       })
    last_name = serializers.CharField(max_length=100,
                                      required=False,
                                      error_messages={
                                          'required': 'Last name is required',
                                          'blank': 'Last name cannot be blank',
                                      })
    photo = serializers.ImageField(required=False)
    phone = serializers.IntegerField(min_value=(10 ** 9),
                                     max_value=(10 ** 10 - 1),
                                     error_messages={
                                         'required': 'Phone number is required',
                                         'blank': 'Phone number cannot be blank',
                                         'min_value': 'Invalid phone number',
                                         'max_value': 'Invalid phone number',
                                         'invalid': 'Invalid phone number'
                                     })


class ProfileEditForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False)
    username = forms.CharField(required=True)
    # first_name = forms.CharField(required=False)
    # last_name = forms.CharField(required=False)
    # phone = forms.CharField(required=False)
    email = forms.EmailField(disabled=True,required=False)

    def clean(self):
        cleaned_data = super(ProfileEditForm, self).clean()
        username = cleaned_data['username']
        if not self.instance.username==username :
            if get_user_model().objects.filter(username=username).exists():
                raise ValidationError({'username':'User name already taken.'})

    class Meta:
        model = get_user_model()
        fields= ('first_name', 'last_name', 'phone_number')


class ProfileView(TemplateView):
    template_name = 'users/profile_view.html'

    def get(self, request, *args, **kwargs):
        user_name = kwargs.get('user_name')
        try:
            if not user_name:
                raise Http404("User name not valid")
            user = get_user_model().objects.get(username=user_name)
            return TemplateResponse(request, self.template_name, context={'user':user})
        except get_user_model().DoesNotExist:
            raise Http404("User does not exist")


class ProfileEdit(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile_edit.html'

    def get(self, request, *args, **kwargs):
        form = ProfileEditForm(initial=request.user.get_profile_initial())
        context = {'form': form}
        context.update(request.user.get_profile_context())
        return TemplateResponse(request, self.template_name, context=context)

    def post(self, request):
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.phone_number = form.cleaned_data['phone_number']
            user.save()
            if form.cleaned_data.get('profile_image'):
                user.profile.photo = form.cleaned_data['profile_image']
                user.profile.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            return TemplateResponse(request, self.template_name, context={'form': form})
