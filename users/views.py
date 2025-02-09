from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout
from django.views import View
from .forms import *
from django.http import Http404
from customization.models import ShablonDict, Settings
from .models import UserProperty, StatusDict
from django.core.mail import send_mail
from softmall.settings import DEFAULT_FROM_EMAIL


def main(request):
    welcome_message = ShablonDict.objects.get(code='WELCOME_MSG')
    return render(request,
                  'main.html', context={'auth': True if request.user.is_authenticated else False,
                                        'welcome_message': welcome_message})


# Выход из аккаунта
def logout_view(request):
    logout(request)
    return redirect('main')


def admin_panel(request):
    if not request.user.is_staff:
        raise Http404("Страница не найдена")
    return render(request,
                  'admin_panel.html', context={'auth': True if request.user.is_authenticated else False})


""" 
Регистрация пользователей
"""
class UserReg(View):
    def get(self, request):
        if not request.user.is_staff:
            raise Http404("Страница не найдена")
        return render(request, 'user_register.html', context={'form': SigUpForm(),
                                                              'auth': True if request.user.is_authenticated else False})

    def post(self, request):
        form = SigUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        else:
            return render(request, 'user_register.html', context={'form': form,
                                                                  'auth': True if request.user.is_authenticated else False})


""" 
Авторизация
"""
class Auth(LoginView):
    form_class = LoginUserForm
    redirect_authenticated_user = True
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_invalid(self, form):
        messages.error(self.request, 'Неправильный логин или пароль')
        return self.render_to_response(self.get_context_data(form=form))


"""
Личный профиль
"""
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        initial_data = {
            'username': user.username,
            'first_name': user.username,
            'last_name': user.lastname,
            'patronymic': user.patronymic}

        return render(request, 'profile.html', context={'form': ProfileForm(initial=initial_data),
                                                           'auth': True, 'user': user})
    else:
        return redirect('main')

"""
Смена пароля
"""
class ChangePassword(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'change_password.html', context={'form': ChangePasswordForm(),
                                                                    'auth': True,})
        else:
            raise Http404("Страница не найдена")

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect('change_password_complete')
        else:
            return render(request, 'change_password.html', context={'form': form,
                                                                    'auth': True,})


def change_password_complete(request):
    return render(request,'change_password_complete.html',
                  context={'auth': True if request.user.is_authenticated else False})


""" 
Рассылка
"""
class SendMail(View):
    def get(self, request):
        if not request.user.is_staff:
            raise Http404("Страница не найдена")
        return render(request, 'send_mail.html',
                      context={'form': SendMailForm()})

    def post(self, request):
        form = SendMailForm(request.POST)
        if form.is_valid():
            theme = form.cleaned_data['theme']
            message = form.cleaned_data['message']
            emails = UserProperty.objects.filter(property__code='USER_EMAIL')
            for email in emails:
                recipient_list = [email.value]
                try:
                    send_mail(theme, message, from_email=DEFAULT_FROM_EMAIL, recipient_list=recipient_list)
                    status = StatusDict.objects.get(code='SENT')
                except:
                    status = StatusDict.objects.get(code='FAILED')
                UserSending.objects.create(user=email.user, status=status, message=message)
                print('ok')
                return redirect('admin_panel')
        else:
            redirect('main')


""" 
Поддержка
"""
def support(request):
    support_email = Settings.objects.get(setting__code='SUPPORT_EMAIL')
    return render(request,'support.html',
                  context={'auth': True if request.user.is_authenticated else False,
                           'support_email':support_email.value})
