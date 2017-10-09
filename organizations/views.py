from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from organizations.models import Organization, OrganizationOnboard


class OrganizationView(LoginRequiredMixin, TemplateView):
    template_name = 'organizations/organization.html'

    def get(self, request, *args, **kwargs):
        try:
            org = Organization.objects.get(id=kwargs['org_name'])
            users = get_user_model().objects.filter(organization=org)
            return TemplateResponse(request, self.template_name, {'org': org, 'users':users})
        except Organization.DoesNotExist:
            raise Http404('Organization does not exist.')
        except KeyError:
            raise Http404('Organization not given')


class OrganizationList(LoginRequiredMixin, APIView):

    def get(self, request):
        orgs = Organization.objects.filter(is_active=True).values_list('name', flat=True)
        data = {item: None for item in orgs}
        return Response(data=data, status=status.HTTP_200_OK)


class OnboardRequestForm(forms.ModelForm):
    class Meta:
        model = OrganizationOnboard
        fields = ['telephone', 'address']

    def save(self, user):
        self.instance.created_by = user
        super(OnboardRequestForm, self).save()

    def clean(self):
        try:
            int(self.cleaned_data.get('phone_no', ' '))
        except:
            raise ValidationError('Telephone number not valid')


class OrganizationOnboardRequest(LoginRequiredMixin, APIView):

    def post(self, request):
        data = request.POST
        form = OnboardRequestForm(data=data)
        if form.is_valid():
            form.save(request.user)
            return Response(data="Your request has been captured", status=status.HTTP_200_OK)
        else:
            return Response(data=form.errors, status=status.HTTP_400_BAD_REQUEST)
