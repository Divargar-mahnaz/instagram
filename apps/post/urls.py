from django.urls import path, re_path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    # after log in each user come home page with his slug
    re_path(r'personal/(?P<slug>[-\w]+)/', Home.as_view(), name='home'),
    # for create post give slug and return form and slug
    re_path(r'new_post/(?P<slug>[-\w]+)', NewPost.as_view(), name='new_post'),
    re_path(r'profile/(?P<slug>[-\w]+)', Profile.as_view(), name='profile'),
    re_path(r'general/(?P<user_slug>[-\w]+)/(?P<owner_slug>[-\w]+)/', GeneralProfile.as_view(), name='general_profile'),
    re_path(r'(?P<slug>[-\w]+)/post_detail/(?P<pk>[-\w]+)/', DetailPost.as_view(), name='post_detail'),
    re_path(r'(?P<user_slug>[-\w]+)/like/(?P<post_pk>[-\w]+)', Like.as_view(), name='like'),
    re_path(r'(?P<user_slug>[-\w]+)/comment/(?P<post_pk>[-\w]+)', LeaveComment.as_view(), name='comment'),
    re_path(r'(?P<user_slug>[-\w]+)/follow/(?P<followed>[-\w]+)', Follow.as_view(), name='follow'),

]
