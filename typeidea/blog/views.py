from datetime import date

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, F
from django.core.cache import cache

from .models import Post, Tag, Category
from config.models import SideBar

# Create your views here.


class CommonViewMinxi:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMinxi, ListView):
    queryset = Post.latest_posts()
    template_name = 'blog/list.html'
    paginate_by = 10
    context_object_name = 'post_list'


#   注意CommonViewMinxi必须写在前面
class PostDetailView(CommonViewMinxi, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    #   DetailView 必须指定url中那个键作为筛选的主键.
    pk_url_kwarg = 'post_id'

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = f'pv:{uid}:{self.request.path}'
        uv_key = f'uv:{uid}:{str(date.today())}:{self.request.path}'
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)  # 一分钟有效
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60)  # 24小时有效
        if increase_pv and increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1, uv=F('uv')+1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv')+1)


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #   如果没有获取到对象就返回404页面。
        category = get_object_or_404(Category, pk=self.kwargs.get('category_id'))
        context.update({'category': category})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('category_id'))
        return queryset


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #   如果没有获取到对象就返回404页面。
        tag = get_object_or_404(Tag, pk=self.kwargs.get('tag_id'))
        context.update({'tag': tag})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tag__id=self.kwargs.get('tag_id'))
        return queryset


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        keyword = self.request.GET.get('keyword', '')
        context.update({'keyword': keyword})
        return context

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()
        keyword = self.request.GET.get('keyword', None)
        if not keyword:
            return queryset
        print("过滤了")
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        author = self.kwargs.get("author")
        queryset = super().get_queryset()
        return queryset.filter(owner=author)

