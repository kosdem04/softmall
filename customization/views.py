from django.shortcuts import render, redirect
from django.views import View
from django.http import Http404
from .forms import *


""" 
Создание кодов системы
"""
class AddSettingDict(View):
    def get(self, request):
        if not request.user.is_staff:
            raise Http404("Страница не найдена")
        return render(request, 'add_settings_dict.html', context={'form': AddSettingDictForm(),
                                                                  'auth': True if request.user.is_authenticated else False})

    def post(self, request):
        form = AddSettingDictForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        else:
            return render(request, 'add_settings_dict.html', context={'form': AddSettingDictForm(),
                                                                  'auth': True if request.user.is_authenticated else False})


""" 
Добавление общих свойств
"""
class AddSetting(View):
    def get(self, request):
        if not request.user.is_staff:
            raise Http404("Страница не найдена")
        return render(request, 'add_settings.html', context={'form': AddSettingForm(),
                                                                  'auth': True if request.user.is_authenticated else False})

    def post(self, request):
        form = AddSettingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        else:
            return render(request, 'add_settings.html', context={'form': form,
                                                                  'auth': True if request.user.is_authenticated else False})


""" 
Список настроек
"""
def show_settings(request):
    if not request.user.is_staff:
        raise Http404("Страница не найдена")
    all_settings = Settings.objects.all()
    return render(request, 'show_settings.html', context={'all_settings': all_settings,
                                                              'auth': True if request.user.is_authenticated else False})


""" 
Изменение настроек
"""
class EditSetting(View):
    def get(self, request, setting_pk):
        if not request.user.is_staff:
            raise Http404("Страница не найдена")
        setting = Settings.objects.get(pk=setting_pk)
        initial_data = {'setting': setting.setting,
                        'value': setting.value,
                        'active_from': setting.active_from,
                        'active_to': setting.active_to,
        }
        return render(request, 'edit_settings.html', context={'form': EditSettingForm(initial=initial_data),
                                                              'setting_pk':setting_pk,
                                                              'auth': True if request.user.is_authenticated else False})

    def post(self, request, setting_pk):
        form = EditSettingForm(request.POST)
        if form.is_valid():
            form.save(setting_pk)
            return redirect('show_settings')
        else:
            return render(request, 'edit_settings.html', context={'form': form,
                                                                  'setting_pk': setting_pk,
                                                                  'auth': True if request.user.is_authenticated else False})


""" 
Удаление настройки
"""
def delete_setting(request, setting_pk):
    if not request.user.is_staff:
        raise Http404("Страница не найдена")
    Settings.objects.get(id=setting_pk).delete()
    return redirect('show_settings')

