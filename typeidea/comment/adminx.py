import xadmin

from .models import Comment
from typeidea.base_admin import BaseOwnAdmin
# Register your models here.


@xadmin.sites.register(Comment)
class CommentAdmin(BaseOwnAdmin):
    list_display = (
        'target', 'content', 'nickname', 'website',
        'email', 'status', 'created_time'
    )
