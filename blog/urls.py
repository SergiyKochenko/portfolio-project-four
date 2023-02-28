from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('about/', views.about_page, name='about'),
    path('pricing/', views.pricing_page, name='pricing'),
    path('gallery/', views.gallery_page, name='gallery'),
    path('contact/', views.contact_page, name='contact'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]
