import xadmin
from django.utils.html import mark_safe
from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter

from .models import Tag, Category, Post
from .adminForm import PostForm
from typeidea.base_admin import BaseOwnAdmin


class PostInline:
    form_layout = (
        Container(
            Row('title', 'desc')
        )
    )
    extra = 1
    model = Post


class CategoryOwnerFilter(RelatedFieldListFilter):
    """ 自定义过滤器只展示当前用户分类 """
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_view, field_path):
        super().__init__(field, request, params, model, model_view, field_path)
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time')
    # fields = ('name', 'status', 'is_nav',)
    form_layout = (
        Fieldset(
            '基础配置',
            'name',
            Row('status', 'is_nav'),
        )
    )

    # inlines = [PostInline]


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnAdmin):
    list_display = ('name', 'status', 'created_time')
    # fields = ('name', 'status')
    form_layout = (
        Fieldset(
            '基础配置',
            'status',
            'name',
        )
    )


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnAdmin):
    list_display = (
        'title', 'category', 'status',
        'owner', 'created_time', 'operator'
    )
    list_display_links = None

    list_filter = ['category']   # 目的是在选择过滤条件的时候只显示自己的分类, 用xadmin的时候要用字段名
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
    # fieldsets = (
    #     ('基础配置', {
    #         'description': '基础配置描述',
    #         'fields': (
    #             ('title', 'category'),
    #             'status',
    #         ),
    #     }),
    #     ('内容', {
    #         'fields': (
    #             'desc',
    #             'content',
    #         ),
    #     }),
    #     ('额外信息', {
    #         'classes': ('collapse', ),
    #         'fields': ('tag', )
    #     })
    # )
    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )

    def operator(self, obj):
        # return f'hh{reverse("admin:blog_post_change", args=(obj.id,))}'
        # cus_admin 是站点的名字, 用xadmin就是xadmin
        # 或者是用xadmin的方法.

        # return mark_safe('<a href="{}">编辑</a>'.format(reverse('xadmin:blog_post_change', args=(obj.id,))))
        return mark_safe('<a href="{}">编辑</a>'.format(self.model_admin_url('change', obj.id)))
    operator.short_description = '操作'

    # @property
    # def media(self):
    #     # xadmin基于bootstrap，这里引入会导致页面出现样式冲突。
    #     media = super().media
    #     media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
    #     media.add_css({
    #         'all': ('https://cdn.bootscc.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css', ),
    #     })
    #     return media


# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = (
#         'object_repr', 'object_id', 'action_flag', 'user',
#         'change_message', 'content_type_id',
#     )
