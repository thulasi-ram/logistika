from django.conf import settings
from django.contrib.auth import login
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User


class SignUpValidator(serializers.Serializer):
    first_name = serializers.CharField(max_length=100,
                                 required=False,
                                 error_messages={
                                     'required': 'Name is required',
                                     'blank': 'Name cannot be blank',
                                 })
    last_name = serializers.CharField(max_length=100,
                                      required=False,
                                      error_messages={
                                          'required': 'Name is required',
                                          'blank': 'Name cannot be blank',
                                      })
    password = serializers.CharField(required=True,
                                     error_messages={
                                         'required': 'Password is required',
                                         'blank': 'Password cannot be blank',
                                     })
    phone = serializers.IntegerField(required=False,
                                      min_value=(10 ** 9),
                                      max_value=(10 ** 10 - 1),
                                      error_messages={
                                          'required': 'Phone number is required',
                                          'blank': 'Phone number cannot be blank',
                                          'min_value': 'Invalid phone number',
                                          'max_value': 'Invalid phone number',
                                          'invalid': 'Invalid phone number'
                                      })
    email = serializers.EmailField(required=True,
                                   error_messages={
                                       'required': 'Email is required',
                                       'invalid': 'Email in invalid',
                                       'blank': 'Email cannot be blank',
                                   })

class SignUp(TemplateView, APIView):
    template_name = 'users/signup.html'
    serializer = SignUpValidator

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.template_name)

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            kwargs = {'first_name': serializer.data.get('first_name', ''),
                      'last_name': serializer.data.get('last_name', ''),
                      'phone_number': serializer.data.get('phone', '')}
            user = User.objects.create_user(serializer.data['email'], serializer.data['password'], **kwargs)
            if user:
                user.backend = settings.AUTHENTICATION_BACKENDS
                login(request, user)
                return HttpResponseRedirect(reverse('logistika:landing'))
        except IntegrityError:
            return Response(data='User with the email already exists', status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response(data='Something went wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={'dev_msg': e.message})
