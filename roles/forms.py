from django import forms
from .models import *
from django.core.exceptions import ValidationError


class UserGroupAddForm(forms.ModelForm):

    class Meta:
        model = UserGroup
        fields = ['company', 'group_name', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'style': 'resize: none;'
            })}


class RoleAddForm(forms.ModelForm):

    class Meta:
        model = RolesDict
        fields = ['code', 'name']


class UserRoleAddForm(forms.ModelForm):

    class Meta:
        model = UserRoles
        fields = ['user', 'role', 'active_from', 'active_to']
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


class FunctionAddForm(forms.ModelForm):

    class Meta:
        model = FunctionsDict
        fields = ['code', 'version']


class RoleFunctionAddForm(forms.ModelForm):

    class Meta:
        model = RoleFunctions
        fields = ['role', 'function']