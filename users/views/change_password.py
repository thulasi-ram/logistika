from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ChangePassword(APIView):

    def post(self, request):
        try:
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return Response('Password changed successfully', status=status.HTTP_200_OK)
            else:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Error occurred while changing passwords", status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={'dev_msg': e.message})