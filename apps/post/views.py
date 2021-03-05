from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from apps.post.forms import CreatePostForm
from apps.post.models import Post, Comment

from apps.user.models import User


class Home(View):
    """
    this class is for redirect user to his home page with his slug for other activities
    """

    def get(self, request, slug):
        user = get_object_or_404(User, slug=slug)
        posts = []
        for post in Post.objects.all():
            if post.publisher in user.following.all():
                posts.append(post)
        return render(request, 'post/home.html', {'user': user, 'posts': posts})


class DetailPost(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, slug=self.kwargs['slug'])  # user how is login
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if post.like.through.objects.filter(post_id=post.id, user_id=user.id).count() == 0:
            context['state'] = 'unlike'
        else:
            context['state'] = 'liked'

        context['user'] = user

        return context


class NewPost(View):
    """
    this class is for create new post with form that we create in forms.py
    for more beauty don`t show slug our other of publisher and handle it in this function with slug that is input
    """

    def get(self, request, slug):
        form = CreatePostForm()
        user = get_object_or_404(User, slug=slug)
        return render(request, 'post/new_post.html', {'form': form, 'user': user})

    def post(self, request, slug):
        publisher = get_object_or_404(User, slug=slug)
        form = CreatePostForm(request.POST, request.FILES or None)
        if form.is_valid():
            user = Post(publisher=publisher,
                        location=form.cleaned_data['location'],
                        image=form.cleaned_data['image'],
                        content=form.cleaned_data['content'], )
            user.save()
            return redirect('/tanks/')  # this is not now

        return render(request, 'post/new_post.html', {'form': form, 'user': publisher})


class Profile(View):
    def get(self, request, slug):
        user = get_object_or_404(User, slug=slug)
        return render(request, 'post/profile.html', {'user': user})


class GeneralProfile(View):
    def get(self, request, user_slug, owner_slug):
        user = get_object_or_404(User, slug=user_slug)
        owner = get_object_or_404(User, slug=owner_slug)
        return render(request, 'post/general_profile.html', {'user': user, 'owner': owner})


class Like(View):
    """
    give user_slug and post_pk if post liked in the past dislike and
     if don`t like in past like it the return to detail_page
    """

    def get(self, request, user_slug, post_pk):
        # p.like.add(user)
        post = get_object_or_404(Post, pk=post_pk)
        user = get_object_or_404(User, slug=user_slug)
        if post.like.through.objects.filter(post_id=post.id, user_id=user.id).count() == 0:
            post.like.add(user)

        else:
            post.like.remove(user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class LeaveComment(View):
    """
    give user_slug and post_pk if post and comment from post method the create comment and save

    """

    def post(self, request, user_slug, post_pk):
        comment = request.POST.get('comment')
        post = get_object_or_404(Post, pk=post_pk)
        user = get_object_or_404(User, slug=user_slug)
        if comment.rstrip() != '':
            caption = Comment(person_id_id=user.id, post_id_id=post.id, content=comment)
            caption.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class Follow(View):
    def get(self, request, user_slug, followed):
        user = get_object_or_404(User, slug=user_slug)
        followed = get_object_or_404(User, slug=followed)
        if User.following.through.objects.filter(from_user_id=user.pk, to_user_id=followed.pk).count() == 0:
            user.following.add(followed)
        else:
            user.following.remove(followed)
        return redirect(reverse('general_profile', args=(user_slug, followed.slug)))
