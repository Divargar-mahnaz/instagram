from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from common.validators import  check_website, check_phone_number, check_user_name
from .follow import Follow
from ..managers import UserManager


def my_slugify_function(content):
    return slugify(content, allow_unicode=True)


class User(AbstractBaseUser, PermissionsMixin):
    """
    this class is create for user info
    """
    user_name = models.CharField('Username', max_length=100, unique=True, validators=[check_user_name])
    image = models.ImageField('Image', upload_to='user', blank=True, null=True, default='user/default_profile.png')
    full_name = models.CharField('Full Name', max_length=100, blank=True)
    GENDER = [('F', 'female'), ('M', 'male')]
    gender = models.CharField('Gender', max_length=1, choices=GENDER, blank=True, null=True)
    bio = models.TextField('Bio', blank=True)
    website = models.CharField('Website', blank=True, max_length=150, validators=[check_website])
    phone_number = models.CharField('Phone number', max_length=11, blank=True, null=True, unique=True,
                                    validators=[check_phone_number])
    email = models.EmailField('Email', blank=True, null=True, unique=True)
    request_to = models.ManyToManyField('user.User', verbose_name='follow', symmetrical=False, through='user.Follow',
                                        related_name='request_from')
    slug = AutoSlugField(populate_from=['user_name'], unique=True, allow_unicode=True,
                         slugify_function=my_slugify_function)
    is_active = models.BooleanField(_('active'), default=True)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)

    objects = UserManager()
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        app_label = 'user'

    @property
    def following(self):
        following = []
        for obj in Follow.objects.filter(from_user=self, accept=True):
            following.append(obj.to_user.id)
        following = User.objects.filter(id__in=following)
        return following

    @property
    def followers(self):
        followers = []
        for obj in Follow.objects.filter(to_user=self, accept=True):
            followers.append(obj.from_user.id)
        followers = User.objects.filter(id__in=followers)
        return followers

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def __str__(self):
        return self.user_name
