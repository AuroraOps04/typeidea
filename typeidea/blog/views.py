from django.shortcuts import render
from django.shortcuts import HttpResponse,render

from .models import Post, Tag, Category
from config.models import SideBar
# Create your views here.


def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None
    if tag_id:
        posts, tag = Post.get_by_tag(tag_id)
    elif category_id:
        posts, category = Post.get_by_category(category_id)
    else:
        posts = Post.latest_posts()

    context = {
        'post_list':posts,
        'tag': tag,
        'category': category,
        'siderbars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    context = {
        'post': Post.objects.filter(status=Post.STATUS_NORMAL, id=post_id).select_related('owner', 'category').first()
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)