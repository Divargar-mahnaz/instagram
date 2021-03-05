from django.urls import path, re_path
from .views import *

urlpatterns = [
    # for login page
    path('login/', Login.as_view(), name='login'),
    # this is for autocomplete field in home page header
    re_path(r'user_autocomplete/(?P<slug>[-\w]+)/', UserAutocomplete.as_view(), name='user_autocomplete'),
    re_path(r'search/(?P<slug>[-\w]+)/', FilterUser.as_view(), name='search_user')
]
