from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'users/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'users/login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class PasswordResetView(View):
    def get(self, request):
        form = PasswordResetForm()
        return render(request, 'users/password_reset.html', {'form': form})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(email=form.cleaned_data['email'])
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_str(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('users/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, 'from@example.com', [user.email])
            return redirect('password_reset_done')
        return render(request, 'users/password_reset.html', {'form': form})

class PasswordResetDoneView(View):
    def get(self, request):
        return render(request, 'users/password_reset_done.html')

class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user)
            return render(request, 'users/password_reset_confirm.html', {'form': form})
        else:
            return render(request, 'users/password_reset_confirm.html', {'error': 'Invalid link'})

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
            return render(request, 'users/password_reset_confirm.html', {'form': form})
        else:
            return render(request, 'users/password_reset_confirm.html', {'error': 'Invalid link'})

class PasswordResetCompleteView(View):
    def get(self, request):
        return render(request, 'users/password_reset_complete.html')
