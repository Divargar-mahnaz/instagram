from django.core.serializers import serialize
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.views.generic import UpdateView
from rest_framework.views import APIView

from apps.user.forms import SignUpForm, UserUpdateForm
from apps.user.models import User
from apps.user.serializers import UserSerializer


class SignUp(View):
    """
    this class is for signup give three required field (contact: can be phone or email,username,password)
    and optional field full name
    that check if contact has phone pattern save it as phone and if has email pattern save as email
    """

    def get(self, request):
        form = SignUpForm()
        return render(request, 'user/sign_up.html', {'form': form})

    def post(self, request):
        import re
        form = SignUpForm(request.POST)

        message = ''
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect(reverse('login'))

        return render(request, 'user/sign_up.html', {'form': form, 'message': message})


class UserAutocomplete(View):
    """
    this class is for auto complete search field in home page
    work with jquery
    give all user except  itself and filter it with term in GET method
    """

    def get(self, request, slug):
        if 'term' in request.GET:
            qs = User.objects.exclude(slug=slug).filter(user_name__icontains=request.GET.get('term'))
            search_result = []
            for user in qs:
                search_result.append(user.slug)
            return JsonResponse(search_result, safe=False)
        return render(request, 'user/search.html')


class FilterUser(APIView):
    def get(self, request, slug):
        user_name = request.GET.get('username')
        if user_name:
            user = User.objects.exclude(slug=slug).filter(user_name__icontains=user_name)
        else:
            user = User.objects.exclude(slug=slug)
        user = UserSerializer(user, many=True)
        return JsonResponse(user.data, safe=False)


class UpdateUserProfile(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user/edit_user.html'

    def get_success_url(self, **kwargs):
        return reverse("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
