from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic import ListView

from blog.views import CommonViewMinxi
from .models import Link


class LinkView(CommonViewMinxi, ListView):
    template_name = 'config/links.html'
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL).order_by('weight')
    context_object_name = 'link_list'
