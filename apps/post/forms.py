from django.forms import ModelForm

from apps.post.models import Post


class PostForm(ModelForm):
    """
    this form use for create post this form has three item
    """

    class Meta:
        model = Post
        fields = ['location', 'content', 'image']



