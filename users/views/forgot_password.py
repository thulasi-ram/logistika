import logging

from django.conf import settings
from django.contrib.auth.views import password_reset
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User

logger = logging.getLogger(__name__)

class ForgotPassword(APIView):

    def dispatch(self, request, **kwargs):
        if request.user and request.user.is_active and request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return super(ForgotPassword, self).dispatch(request, **kwargs)

    def get(self, request):
        kwargs = {'post_reset_redirect': reverse_lazy('users:password_reset'),
                  'from_email': settings.SERVER_EMAIL, 'template_name': 'users/password_reset_form.html'}
        response = password_reset(request, **kwargs)
        return response

    def post(self, request):
        kwargs = {'post_reset_redirect': reverse_lazy('users:password_reset'),
                  'from_email': settings.SERVER_EMAIL}
        try:
            data = request.DATA
            if User.objects.filter(email=data['email']).exists():
                response = password_reset(request, **kwargs)
                return Response({'success': 'success', 'msg': 'Mail with password reset instructions sent to the given email'})
            else:
                return Response({'success': 'error', 'msg': 'Invalid user email'})
        except:
            logger.exception("Error in forgot password")
            return Response({'success': 'error', 'msg': 'Forgot password failed due to unknown reasons'})

