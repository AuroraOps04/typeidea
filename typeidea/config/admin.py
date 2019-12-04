from django.contrib import admin

from .models import Link, SideBar
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnAdmin
# Register your models here.


@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnAdmin):
    list_display = (
        'title', 'href', 'weight',
        'owner', 'created_time',
    )

    fields = (
        'title',
        'href',
        'weight'
    )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@admin.register(SideBar, site=custom_site)
class SideBarAdmin(BaseOwnAdmin):
    list_display = (
        'title',
        'display_type',
        'content',
        'status',
        'owner',
        'created_time',
    )

    fields = (
        'title',
        'display_type',
        'content',
        'status',
    )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)