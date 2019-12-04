from django.contrib import admin

from .models import Comment
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnAdmin
# Register your models here.


@admin.register(Comment, site=custom_site)
class CommentAdmin(BaseOwnAdmin):
    list_display = (
        'target', 'content', 'nickname', 'website',
        'email', 'status', 'created_time'
    )