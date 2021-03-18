from django import template
from django.shortcuts import get_object_or_404

register = template.Library()
from apps.user.models import User
from apps.post.models import Post


@register.simple_tag
def get_img(model, slug):
    if model == 'User':
        obj = get_object_or_404(User, slug=slug)
    elif model == 'Post':
        obj = get_object_or_404(Post, slug=slug)
    return obj.image.url


@register.simple_tag
def get_user(model, id):
    """
    giv id of user and return user
    """
    if model == 'User':
        obj = get_object_or_404(User, pk=id)
    elif model == 'Post':
        obj = get_object_or_404(Post, pk=id)
    return obj


@register.simple_tag
def like_number(post):
    """
    count like of special post
    """
    return post.like.count()


@register.simple_tag
def comment_number(post):
    """
    count comment of special post
    """
    return post.comment_set.count()


@register.simple_tag
def get_all_user(login_user):
    return User.objects.exclude(user_name=login_user.user_name)[:10]


