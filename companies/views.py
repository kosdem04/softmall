from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout
from django.views import View
from .forms import *
from django.http import Http404


""" 
Добавление компании
"""
class AddCompany(View):
    def get(self, request):
        if not request.user.is_staff:
            raise Http404("Страница не найдена")
        return render(request, 'add_company.html', context={'form': AddCompanyForm(),
                                                                  'auth': True if request.user.is_authenticated else False})

    def post(self, request):
        form = AddCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        else:
            return render(request, 'add_company.html', context={'form': form,
                                                                  'auth': True if request.user.is_authenticated else False})


""" 
Информация о компании
"""
def company_info(request, company_pk):
    if request.user.company.id != company_pk:
        raise Http404("Страница не найдена")
    company = Company.objects.get(id=company_pk)
    return render(request, 'company_info.html', context={'company': company,
                                                              'auth': True if request.user.is_authenticated else False})
