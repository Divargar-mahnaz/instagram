from django.db import models
import hashlib
from common.validators import check_password, check_website, check_phone_number, check_user_name
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField


def my_slugify_function(content):
    return slugify(content, allow_unicode=True)


class User(models.Model):
    """
    this class is create for user info
    """
    user_name = models.CharField('Username', max_length=100, unique=True, validators=[check_user_name])
    password = models.CharField('Password', max_length=64, validators=[check_password])
    image = models.ImageField('Image', upload_to='user', blank=True, null=True, default='user/default_profile.png')
    full_name = models.CharField('Full Name', max_length=100, blank=True)
    GENDER = [('F', 'female'), ('M', 'male')]
    gender = models.CharField('Gender', max_length=1, choices=GENDER, blank=True, null=True)
    bio = models.TextField('Bio', blank=True)
    website = models.CharField('Website', blank=True, max_length=150, validators=[check_website])
    phone_number = models.CharField('Phone number', max_length=11, blank=True, null=True, unique=True,
                                    validators=[check_phone_number])
    email = models.EmailField('Email', blank=True, null=True, unique=True)
    following = models.ManyToManyField('self', verbose_name='follow', blank=True, symmetrical=False,
                                       related_name='followers')
    slug = AutoSlugField(populate_from=['user_name'], unique=True, allow_unicode=True,
                         slugify_function=my_slugify_function)

    def save(self, *args, **kwargs):
        """
        we want to hash password so before save convert it
        """
        if self.id is None:
            self.password = hashlib.sha256(self.password.encode('utf-8')).hexdigest()

        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.user_name
