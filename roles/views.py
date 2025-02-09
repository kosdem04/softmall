from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout
from django.views import View
from .forms import *
from django.http import Http404


""" 
Создание ролей
"""
class RoleAdd(View):
    def get(self, request):
        if not request.user.is_staff:
            raise Http404("Страница не найдена")
        return render(request, 'role_add.html', context={'form': RoleAddForm(),
                                                                  'auth': True if request.user.is_authenticated else False})

    def post(self, request):
        form = RoleAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        else:
            return render(request, 'role_add.html', context={'form': form,
                                                                  'auth': True if request.user.is_authenticated else False})


""" 
Добавление ролей пользователям
"""
class UserRoleAdd(View):
    def get(self, request):
        if not request.user.is_staff:
            raise Http404("Страница не найдена")
        return render(request, 'user_role_add.html', context={'form': UserRoleAddForm(),
                                                                  'auth': True if request.user.is_authenticated else False})

    def post(self, request):
        form = UserRoleAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        else:
            return render(request, 'user_role_add.html', context={'form': form,
                                                                  'auth': True if request.user.is_authenticated else False})

""" 
Создание групп пользователей
"""
class UserGroupAdd(View):
    def get(self, request):
        if not request.user.is_staff:
            raise Http404("Страница не найдена")
        return render(request, 'user_group_add.html', context={'form': UserGroupAddForm(),
                                                                  'auth': True if request.user.is_authenticated else False})

    def post(self, request):
        form = UserGroupAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        else:
            return render(request, 'user_group_add.html', context={'form': form,
                                                                  'auth': True if request.user.is_authenticated else False})


""" 
Создание функций
"""
class FunctionAdd(View):
    def get(self, request):
        if not request.user.is_staff:
            raise Http404("Страница не найдена")
        return render(request, 'function_add.html', context={'form': FunctionAddForm(),
                                                                  'auth': True if request.user.is_authenticated else False})

    def post(self, request):
        form = FunctionAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        else:
            return render(request, 'function_add.html', context={'form': form,
                                                                  'auth': True if request.user.is_authenticated else False})



""" 
Распределение функций по ролям
"""
class RoleFunctionAdd(View):
    def get(self, request):
        if not request.user.is_staff:
            raise Http404("Страница не найдена")
        return render(request, 'role_function_add.html', context={'form': RoleFunctionAddForm(),
                                                                  'auth': True if request.user.is_authenticated else False})

    def post(self, request):
        form = RoleFunctionAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        else:
            return render(request, 'role_function_add.html', context={'form': form,
                                                                  'auth': True if request.user.is_authenticated else False})



