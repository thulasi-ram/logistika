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

from users.models import User, Profile


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

    def save(self, **kwargs):
        kwargs = {'first_name': self.validated_data.get('first_name', ''),
                  'last_name': self.validated_data.get('last_name', ''),
                  'phone_number': self.validated_data.get('phone', '')}
        user = User.objects.create_user(self.validated_data['email'], self.validated_data['password'], **kwargs)
        return user


class SignUp(TemplateView):
    template_name = 'users/signup.html'

    def dispatch(self, request, **kwargs):
        if request.user and request.user.is_active and request.user.is_authenticated():
            return HttpResponseRedirect(reverse('landing'))
        return super(SignUp, self).dispatch(request, **kwargs)

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.template_name)


class SignupAPI(APIView):
    serializer = SignUpValidator

    def dispatch(self, request, **kwargs):
        if request.user and request.user.is_active and request.user.is_authenticated():
            return Response(data='{user} with the email already logged in. Please refresh.'.format(user=request.user.get_short_name()), status=status.HTTP_409_CONFLICT)
        return super(SignupAPI, self).dispatch(request, **kwargs)

    def post(self, request):
        try:
            data = request.POST
            serializer = self.serializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()
            if user:
                login(request, user)
                Profile.objects.create(user=user)
                # user.backend = settings.AUTHENTICATION_BACKENDS
                return Response(data={'redirect': reverse('landing')}, status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response(data='User with the email already exists', status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response(data='Something went wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            headers={'dev_msg': e.message})