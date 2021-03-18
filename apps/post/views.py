from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView
from apps.post.forms import PostForm
from apps.post.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.user.models import User, Follow
from django.utils.translation import ugettext_lazy as _


class Home(LoginRequiredMixin, View):
    """
    this class is for redirect user to his home page with his slug for other activities
    """

    def get(self, request):
        user = request.user
        posts = []
        for post in Post.objects.all():

            # if publisher is in following(who user sent request and accepted)
            if post.publisher in user.following:
                posts.append(post)
        return render(request, 'post/home.html', {'posts': posts})


class DetailPost(LoginRequiredMixin, DetailView):
    """
    show detail of post
    """
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user  # user how is login
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if post.like.through.objects.filter(post_id=post.id, user_id=user.id).count() == 0:
            context['state'] = 'unlike'
        else:
            context['state'] = 'liked'
        return context


class NewPost(LoginRequiredMixin, View):
    """
    this class is for create new post with form that we create in forms.py
    for more beauty don`t show slug our other of publisher and handle it in this function with slug that is input
    """

    def get(self, request):
        form = PostForm()
        return render(request, 'post/new_post.html', {'form': form})

    def post(self, request):
        publisher = request.user
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = Post(publisher=publisher,
                        location=form.cleaned_data['location'],
                        image=form.cleaned_data['image'],
                        content=form.cleaned_data['content'], )
            post.save()
            return redirect(reverse('profile'))

        return render(request, 'post/new_post.html', {'form': form})


class UpdatePost(LoginRequiredMixin, UpdateView):
    """
    give post id and edit it then return to user profile
    """
    model = Post
    template_name = 'post/new_post.html'
    form_class = PostForm
    def get_success_url(self, **kwargs):
        return reverse_lazy("profile")


class DeletePost(LoginRequiredMixin, DeleteView):
    """ delete selected post """
    model = Post

    def get_success_url(self, **kwargs):
        return reverse_lazy("profile")


class GeneralProfile(LoginRequiredMixin, View):
    """
    this view render html that is profile of user with lower acces only see not edit post or edit profile
    """

    def get(self, request, owner_slug):
        owner = get_object_or_404(User, slug=owner_slug)
        return render(request, 'post/general_profile.html', {'owner': owner})


class Like(LoginRequiredMixin, View):
    """
    give user_slug and post_pk if post liked in the past dislike and
     if don`t like in past like it the return to detail_page
    """

    def get(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        user = request.user
        if post.like.through.objects.filter(post_id=post.id, user_id=user.id).count() == 0:
            post.like.add(user)

        else:
            post.like.remove(user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class LeaveComment(LoginRequiredMixin, View):
    """
    give user_slug and post_pk if post and comment from post method the create comment and save

    """

    def post(self, request, post_pk):
        comment = request.POST.get('comment')
        post = get_object_or_404(Post, pk=post_pk)
        user = request.user
        if comment.rstrip() != '':
            caption = Comment(person_id_id=user.id, post_id_id=post.id, content=comment)
            caption.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class DeleteComment(LoginRequiredMixin, DeleteView):
    """
    delete selected comment
    """
    model = Comment

    def get_success_url(self, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        url = "%s?next=profile" % reverse("post_detail", args=(comment.post_id_id,))
        return url


class Request(LoginRequiredMixin, View):
    """
    this class use when user click on follow btn and save request
    """

    def get(self, request, followed):
        user = request.user
        followed = get_object_or_404(User, slug=followed)
        if User.request_to.through.objects.filter(from_user_id=user.pk, to_user_id=followed.pk).count() == 0:
            req = Follow(from_user=user, to_user=followed, accept=False)
            req.save()
        else:
            req = Follow.objects.get(from_user=user, to_user=followed)
            req.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CancelRequest(LoginRequiredMixin, View):
    """
    this class use when user click on follow btn and save request
    """

    def get(self, request, send_request):
        user = request.user
        send_request = get_object_or_404(User, slug=send_request)
        req = Follow.objects.get(from_user=send_request, to_user=user)
        req.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class FollowView(LoginRequiredMixin, View):
    """
    user can accept or delete requests
    """

    def get(self, request, followed):
        user = request.user
        applicant = get_object_or_404(User, slug=followed)
        req = Follow.objects.get(from_user=applicant, to_user=user)
        req.accept = True
        req.save()
        return redirect(
            to="{}?current_followed={}".format(reverse('account_activity'), str(applicant)))


class AccountActivity(LoginRequiredMixin, View):
    """
    if some one send request show to user
    """
    def get(self, request):
        user = request.user
        applicants = Follow.objects.filter(to_user=user, accept=False)
        return render(request, 'post/account_activity.html', {'applicants': applicants})
