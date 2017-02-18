from django import forms
from django.contrib.auth import authenticate, login
from django.db.migrations import serializer
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User


class LoginValidator(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={
        'required': 'User email is required',
        'blank': 'User email cannot be blank'
    })
    password = serializers.CharField(required=True, error_messages={
        'required': 'Password is required',
        'blank': 'Password cannot be blank'
    })


class Login(TemplateView, APIView):
    template_name = 'users/login.html'
    serializer = LoginValidator

    def dispatch(self, request, **kwargs):
        if request.user and request.user.is_active and request.user.is_authenticated():
            return HttpResponseRedirect(reverse('landing'))
        return super(Login, self).dispatch(request, **kwargs)

    def get(self, request, *args, **kwargs):
        data = request.GET
        return TemplateResponse(request, self.template_name, context={'next': data['next'] if data.get('next') else reverse('landing')})

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(username=serializer.data['email'], password=serializer.data['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return Response(data={'redirect': data['next'] if data.get('next') else reverse('landing')}, status=status.HTTP_200_OK)
                else:
                    return Response('User not active', status=status.HTTP_403_FORBIDDEN)
            else:
                if User.objects.filter(email__iexact=serializer.data['email']):
                    return Response(data='Invalid password', status=status.HTTP_400_BAD_REQUEST)
                return Response(data='User not found', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data='Something went wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={'dev_msg': e.message})

