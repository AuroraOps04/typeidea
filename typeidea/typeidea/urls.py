"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.conf.urls import url, include
from django.conf.urls.static import static

from blog.views import (
    IndexView, CategoryView,
    TagView, PostDetailView,
    SearchView, AuthorView,
)
from config.views import LinkView
from comment.views import CommentView
from blog.rss import LatestPostFeed
from blog.sitemap import PostSiteMap
from .autocomplete import CategoryAutocomplete, TagAutocomplete

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category_list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag_list'),
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post_detail'),
    url(r'^links/$', LinkView.as_view(), name='links'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^author/(?P<author>\d+)/$', AuthorView.as_view(), name='author_list'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'^category_autocomplete/$', CategoryAutocomplete.as_view(), name="category_autocomplete"),
    url(r'^tag_autocomplete', TagAutocomplete.as_view(), name="tag_autocomplete"),
    url(r'^xadmin/', xadmin.site.urls, name='xadmin'),
    url(r'^super_admin/', admin.site.urls, name='super_admin'),
    url('^rss|feed/', LatestPostFeed(), name='res'),
    url('^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSiteMap}}),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),  # 这里提供了两个接口，上传图片和查看图片

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # 这个功能是django内置的静态文件处理功能，来处理静态文件的访问。

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns