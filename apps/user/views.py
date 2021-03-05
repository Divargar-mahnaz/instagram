from django.core.serializers import serialize
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
import hashlib

from rest_framework.views import APIView

from apps.user.forms import SignUpForm, LoginForm
from apps.user.models import User
from apps.user.serializers import UserSerializer
from common.constant import PHONE_PATTERN, EMAIL_PATTERN
from django.db import IntegrityError


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
            if re.search(PHONE_PATTERN, form.cleaned_data['contact']):
                try:
                    user = User(user_name=form.cleaned_data['user_name'],
                                password=form.cleaned_data['password'],
                                full_name=form.cleaned_data['full_name'],
                                phone_number=form.cleaned_data['contact'])
                    user.save()
                    return redirect(reverse('login'))
                except IntegrityError as e:  # because phone and email are unique
                    if 'UNIQUE constraint failed:' in e.args[0]:
                        message = 'phone is not unique'

            elif re.search(EMAIL_PATTERN, form.cleaned_data['contact']):
                try:
                    user = User(user_name=form.cleaned_data['user_name'],
                                password=form.cleaned_data['password'],
                                full_name=form.cleaned_data['full_name'],
                                email=form.cleaned_data['contact'])
                    user.save()
                    return redirect(reverse('login'))
                except IntegrityError as e:  # because phone and email are unique
                    if 'UNIQUE constraint failed:' in e.args[0]:
                        message = 'email  is not unique'

        return render(request, 'user/sign_up.html', {'form': form, 'message': message})


class Login(View):
    """
    for login give two required field username and password
    username can be username, email and phone because are unique
    """

    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        username = request.POST.get('user_name')
        password = hashlib.sha256(request.POST.get('password').encode('utf-8')).hexdigest()
        user = User.objects.filter(
            (Q(user_name=username) | Q(phone_number=username) | Q(email=username)) & Q(password=password))
        if user:
            return redirect(reverse('home', args=(user[0].slug,)))
        else:
            message = 'Sorry, your password or username was incorrect.'

        return render(request, 'user/login.html', {'form': form, 'message': message})


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
        print(user_name)
        if user_name:
            user = User.objects.exclude(slug=slug).filter(user_name__icontains=user_name)
        else:
            user = User.objects.exclude(slug=slug)
        user = UserSerializer(user, many=True)
        return JsonResponse(user.data, safe=False)
