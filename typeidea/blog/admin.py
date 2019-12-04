from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe
from django.contrib.admin.models import LogEntry

from .models import Tag, Category, Post
from .adminForm import PostForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnAdmin
# Register your models here.


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类 """
    title = '分类过滤器'
    parameter_name = 'owner_category'   # url里面的参数名

    def lookups(self, request, model_admin):
        """ 这个函数是做分类名和url里面对应的参数的映射关系。"""
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()  # 取出来是url里面传递过来的值。
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time')
    fields = ('name', 'status', 'is_nav',)


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnAdmin):
    list_display = (
        'title', 'category', 'status',
        'owner', 'created_time', 'operator'
    )
    list_display_links = None

    list_filter = [CategoryOwnerFilter, ]   # 目的是在选择过滤条件的时候只显示自己的分类
    # list_filter = ['category', ]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    filter_horizontal = ('tag', )

    form = PostForm
    # 编辑页面
    save_on_top = True

    # fields = (
    #     ('category', 'title'),  # 这代表放在一行.
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse', ),
            'fields': ('tag', )
        })
    )

    def operator(self, obj):
        # return f'hh{reverse("admin:blog_post_change", args=(obj.id,))}'
        # cus_admin 是站点的名字
        return mark_safe('<a href="{}">编辑</a>'.format(reverse('cus_admin:blog_post_change', args=(obj.id,))))
    operator.short_description = '操作'


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        'object_repr', 'object_id', 'action_flag', 'user',
        'change_message', 'content_type_id',
    )
