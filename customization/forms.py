from django import forms
from .models import *
from django.core.exceptions import ValidationError


class AddSettingDictForm(forms.ModelForm):

    class Meta:
        model = SettingsDict
        fields = ['code', 'name']


class AddSettingForm(forms.ModelForm):

    class Meta:
        model = Settings
        fields = ['setting', 'value', 'active_from', 'active_to']
        widgets = {
            'active_from': forms.DateInput(attrs={'type': 'date'}),
            'active_to': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        active_from = cleaned_data.get("active_from")
        active_to = cleaned_data.get("active_to")

        if active_from and active_to and active_to < active_from:
            raise ValidationError({"active_to": "Дата окончания не может быть меньше даты начала."})

        return cleaned_data


class EditSettingForm(forms.ModelForm):

    class Meta:
        model = Settings
        fields = ['setting', 'value', 'active_from', 'active_to']

    def clean(self):
        cleaned_data = super().clean()
        active_from = cleaned_data.get("active_from")
        active_to = cleaned_data.get("active_to")

        if active_from and active_to and active_to < active_from:
            raise ValidationError({"active_to": "Дата окончания не может быть меньше даты начала."})

        return cleaned_data

    def save(self, setting_pk):
        Settings.objects.filter(pk=setting_pk).update(
            setting=self.cleaned_data['setting'],
            value=self.cleaned_data['value'],
            active_from=self.cleaned_data['active_from'],
            active_to=self.cleaned_data['active_to'] )




