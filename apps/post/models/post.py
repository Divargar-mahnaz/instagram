from django.db import models
from .comment import Comment
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Post(models.Model):
    """
    this class is for post ,
    create_date is auto and self create with out user
    publisher is how create post
    evre post can have many like and coment
    """
    create_date = models.DateTimeField(auto_now_add=True)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(_('Location'), max_length=200, blank=True)
    image = models.ImageField(_('Image'), upload_to='posts')
    content = models.TextField(_('Content'), blank=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('Like'), blank=True,
                                  related_name='likes_set')
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('comment'), through=Comment,
                                      related_name='comments_set')

    class Meta:
        ordering = ['-create_date']

    @property
    def age(self):
        """
        this function is for show how long past from post published
        recently if less than 1 hour
        number of hours if more than one hour
        number of day if more than one day
        number of month if more than one month
        and else number of year
        :return: string base on explain
        """
        import calendar
        now = timezone.now()
        age = now - self.create_date
        if age.days == 0 and age.seconds < 3600:
            return str(_(' recently '))
        if age.days == 0:
            return str(age.seconds // 3600) + str(_('  hours ago '))
        if age.days < calendar.monthrange(self.create_date.year, self.create_date.month)[1]:
            return str(age.days) + str(_(' days ago '))
        if age.days < 365:
            result = 0
            days = age.days
            month = self.create_date.month
            year = self.create_date.year
            for i in range(1, 13):
                if month > 12:
                    month = 1
                    year += 1
                days -= calendar.monthrange(year, month)[1]
                if days > 0:
                    month += 1
                    result += 1
                elif days == 0:
                    word = str(_(' month ago'))
                    if result > 1:
                        word = str(_(' months ago'))
                    return str(result + 1) + word
                else:
                    word = str(_(' month ago'))
                    if result > 1:
                        word = str(_(' months ago'))
                    return str(result) + word
        if age.days >= 365:
            year = age.days // 365
            word = str(_(' year ago'))
            if year > 1:
                word = str(_(' years ago'))
            return str(year) + word

    def __str__(self):
        return self.publisher.user_name + ':' + self.content[:10] + '...'
