from . import views
from django.urls import path
# ================
from django.contrib import admin
admin.site.site_header = 'Blog site Administration'
from django.contrib import admin
admin.site.site_title = 'Blog Site'
from django.contrib import admin
admin.site.index_title= 'Admin Site'
# ==================
urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('about/', views.about_page, name='about'),
    path('usersblog/', views.usersblog_page, name='usersblog'),
    path('create-post/', views.create_post, name='create-post'),
    path('pricing/', views.pricing_page, name='pricing'),
    path('gallery/', views.gallery_page, name='gallery'),
    path('contact/', views.contact_page, name='contact'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('<str:slug>', views.usersblog_detail, name='usersblog_detail'),
]