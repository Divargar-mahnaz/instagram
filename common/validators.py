from django.core.exceptions import ValidationError
from .constant import WEBSITE_PATTERN, PASSWORD_PATTERN, PHONE_PATTERN, USERNAME_PATTERN
import re
from django.utils.translation import ugettext_lazy as _

def check_password(password):
    """
    check value of password field in user model with pattern for sure it`s correct or not
    """
    pattern = PASSWORD_PATTERN
    if not re.search(pattern, password):
        raise ValidationError(_('your password must be at least 8 character and  digit and upper and lower letter'))


def check_website(website):
    """
        check value of website field in user model with pattern for sure it`s correct or not
    """
    pattern = WEBSITE_PATTERN
    if not re.search(pattern, website):
        raise ValidationError(_('your website is invalid'))


def check_phone_number(phone):
    """
    check value of phone field in user model with pattern for sure it`s correct or not
    """
    pattern = PHONE_PATTERN
    if not re.search(pattern, phone):
        raise ValidationError(_('your phone number is invalid'))


def check_user_name(user_name):
    """
        check value of user_name field in user model with pattern for sure it`s correct or not
    """
    pattern = USERNAME_PATTERN
    if not re.search(USERNAME_PATTERN, user_name):
        raise ValidationError(_('invalid user name'))
