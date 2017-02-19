from string import Template

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import widgets, ClearableFileInput, TextInput
from rest_framework import serializers


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


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        context = {'profile_url': request.user}
        return TemplateResponse(request, self.template_name, context=context)

    def post(self, request):
        data = request.POST
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            context = {'profile_url': request.user}
        else:
            context = {'form_errors': serializer.errors}
        return TemplateResponse(request, self.template_name, context=context)
