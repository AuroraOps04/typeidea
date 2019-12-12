import xadmin
from xadmin.layout import Fieldset

from .models import SideBar, Link
from typeidea.base_admin import BaseOwnAdmin
# Register your models here.


@xadmin.sites.register(Link)
class LinkAdmin(BaseOwnAdmin):
    list_display = (
        'title', 'href', 'weight',
        'owner', 'created_time',
    )

    form_layout = (
        Fieldset(
            '基础配置',
            'title',
            'href',
            'weight'
        )
    )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@xadmin.sites.register(SideBar)
class SideBarAdmin(BaseOwnAdmin):
    list_display = (
        'title',
        'display_type',
        'content',
        'status',
        'owner',
        'created_time',
    )

    form_layout = (
        Fieldset(
            '基础配置',
            'title',
            'status',
        ),
        Fieldset(
            '内容配置',
            'display_type',
            'content',
        )
    )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)