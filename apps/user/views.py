import json

import pyotp
from django.core.serializers import serialize
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.generic import UpdateView
from rest_framework.views import APIView

from apps.user.forms import SignUpForm, UserUpdateForm
from apps.user.models import User
from apps.user.serializers import UserSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
import ghasedak
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import activate

activate('fa')


class SignUp(View):
    """
    this class is for signup give three required field ( phone or email,username,password)
    and optional field full name
    then redirect to send validation sms or validation email
    """

    def get(self, request):
        form = SignUpForm()
        return render(request, 'user/sign_up.html', {'form': form})

    def post(self, request):
        import re
        form = SignUpForm(request.POST)
        verification_way = request.POST.get('verification')
        print(verification_way)
        message = ''
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            if form.cleaned_data['phone_number'] and form.cleaned_data['email'] and verification_way:
                if verification_way == 'email':
                    return redirect(reverse('send-email', args=(user.slug,)))
                elif verification_way == 'phone':
                    return redirect(reverse('send-sms', args=(user.slug,)))
            elif form.cleaned_data['phone_number']:
                return redirect(reverse('send-sms', args=(user.slug,)))
            else:
                return redirect(reverse('send-email', args=(user.slug,)))
        print(form.errors)
        return render(request, 'user/sign_up.html', {'form': form, 'message': message})


class SendEmailVerification(View):
    """
    create message and send to user with mail
    """

    def get(self, request, user_slug):
        user = get_object_or_404(User, slug=user_slug)
        print(user)
        print(urlsafe_base64_encode(force_bytes(user.pk)).encode().decode())
        current_site = get_current_site(request)
        mail_subject = 'Activate your instagram account.'
        message = render_to_string('user/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
            'token': account_activation_token.make_token(user),
        })

        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return render(request, 'user/wait_for_email.html', {'user': user})


class EmailVerify(View):
    """
    when user verify email that send to him then activate account
    """

    def get(self, request, uidb64, token):
        try:
            from apps.user.models import User
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(reverse('login'))
        else:
            return HttpResponse(_('Activation link is invalid!'))


class SendSmsVerification(View):
    """
    send sms to user by number that create by pyotp
    """

    def get(self, request, user_slug):
        sms = ghasedak.Ghasedak("a4405434b82dd6d46e4a88f0ef89d0d71c190265c87e8f883e34e73fe5ef8799")
        user = get_object_or_404(User, slug=user_slug)
        time_otp = pyotp.TOTP(user.key, interval=120)
        time_otp = time_otp.now()
        print(time_otp)
        sms.send(
            {'message': " Your verification code is " + time_otp, 'receptor': user.phone_number,
             'linenumber': "10008566"})
        return redirect(reverse('mobile_verify', args=(user.slug,)))


class MobileVerify(View):
    """
    when user enter code change is active to 1
    """

    def get(self, request, user_slug):
        user = get_object_or_404(User, slug=user_slug)
        return render(request, 'user/mobile_verify.html', {'user': user})

    def post(self, request, user_slug):
        user = get_object_or_404(User, slug=user_slug)
        code = request.POST.get('code')
        if user.authenticate(code):
            user.is_active = True
            user.save()
            return redirect(reverse('login'))

        return render(request, 'user/mobile_verify.html', {'user': user})


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
        serialized_user = UserSerializer(user, many=True)
        try:
            result = serialized_user.data
        except:
            result_list = list(user.values('user_name', 'image', 'slug'))
            for item in result_list:
                item['image'] = '/media/' + item['image']
            return HttpResponse(json.dumps(result_list))
        return JsonResponse(result, safe=False)


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
