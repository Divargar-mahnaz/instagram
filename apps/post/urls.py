from django.urls import path, re_path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [

    re_path(r'personal/', Home.as_view(), name='home'),
    re_path(r'new_post/', NewPost.as_view(), name='new_post'),
    re_path(r'update_post/(?P<pk>[-\w]+)', UpdatePost.as_view(), name='update_post'),
    re_path(r'delete_post/(?P<pk>[-\w]+)', DeletePost.as_view(), name='delete_post'),
    re_path(r'profile/', TemplateView.as_view(template_name='post/profile.html'), name='profile'),
    re_path(r'general/(?P<owner_slug>[-\w]+)/', GeneralProfile.as_view(), name='general_profile'),
    re_path(r'post_detail/(?P<pk>[-\w]+)/', DetailPost.as_view(), name='post_detail'),
    re_path(r'like/(?P<post_pk>[-\w]+)', Like.as_view(), name='like'),
    re_path(r'comment/(?P<post_pk>[-\w]+)', LeaveComment.as_view(), name='comment'),
    re_path(r'comment_delete/(?P<pk>[-\w]+)', DeleteComment.as_view(), name='comment_delete'),
    re_path(r'request/(?P<followed>[-\w]+)', Request.as_view(), name='request'),
    re_path(r'request_cancel/(?P<send_request>[-\w]+)', CancelRequest.as_view(), name='cancel_request'),
    re_path(r'follow/(?P<followed>[-\w]+)', FollowView.as_view(), name='follow'),
    re_path(r'account_activity/', AccountActivity.as_view(), name='account_activity'),

]
