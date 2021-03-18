import pyotp
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from common.validators import check_website, check_phone_number, check_user_name
from .follow import Follow
from ..managers import UserManager


def my_slugify_function(content):
    return slugify(content, allow_unicode=True)


class User(AbstractBaseUser, PermissionsMixin):
    """
    this class is create for user info
    """
    user_name = models.CharField(_('Username'), max_length=100, unique=True, validators=[check_user_name])
    image = models.ImageField(_('Image'), upload_to='user', blank=True, null=True, default='user/default_profile.png')
    full_name = models.CharField(_('Full Name'), max_length=100, blank=True)
    GENDER = [('F', _('female')), ('M', _('male'))]
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER, blank=True, null=True)
    bio = models.TextField(_('Bio'), blank=True, max_length=100)
    website = models.CharField(_('Website'), blank=True, max_length=150, validators=[check_website])
    phone_number = models.CharField(_('Phone number'), max_length=11, blank=True, null=True, unique=True,
                                    validators=[check_phone_number])
    key = models.CharField(max_length=100, unique=True, blank=True)
    email = models.EmailField(_('Email'), blank=True, null=True, unique=True)

    request_to = models.ManyToManyField('user.User', verbose_name=_('follow'), symmetrical=False, through='user.Follow',
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

    def authenticate(self, otp):
        """ This method authenticates the given otp"""
        provided_otp = 0
        try:
            provided_otp = int(otp)
        except:
            return False
        # Here we are using Time Based OTP. The interval is 120 seconds.
        # otp must be provided within this interval or it's invalid
        t = pyotp.TOTP(self.key, interval=120)
        return t.verify(provided_otp)

    def __str__(self):
        return self.user_name
