from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.shortcuts import render

# Create your views here.
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from itertools import chain

from notifications.models import Notifications


class NotificationsFeed(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/notifications.html'

    def get(self, request, *args, **kwargs):
        notifs = Notifications.objects.filter(user=request.user).order_by('-created_at')
        notifs.filter(status=Notifications.UNREAD,
                      created_at__lte=request.user.profile.last_read_notif_time).update(status=Notifications.READ)
        request.user.profile.last_read_notif_time = datetime.now()
        request.user.profile.save()
        page = request.GET.get('page')
        items_per_page = request.META.get('items_per_page', 10)
        paginator = Paginator(notifs, items_per_page)
        try:
            clients = paginator.page(page)
        except PageNotAnInteger:
            clients = paginator.page(1)
        except EmptyPage:
            clients = paginator.page(paginator.num_pages)
        page = clients.number
        return TemplateResponse(request, self.template_name, {'notifs': notifs})
