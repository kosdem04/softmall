from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser, UserSending
from django.contrib.auth import authenticate
from customization.models import ShablonDict


class SigUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'firstname', 'lastname', 'patronymic', 'company', 'group', 'timezone']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def clean_group(self):
        group = self.cleaned_data.get('group')
        company = self.cleaned_data.get('company')
        if company != group.company:
            raise forms.ValidationError("Группа должна соответствовать выбранной компании")
        return group

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'firstname', 'lastname', 'patronymic', 'company', 'group', 'timezone']


class LoginUserForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        blocked_message = ShablonDict.objects.get(code='ACCOUNT_BLOCKED')
        user = CustomUser.objects.filter(username=username).first()
        if user:
            try:
                self.confirm_login_allowed(user)
            except:
                raise forms.ValidationError(blocked_message.value)

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()

        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите новый пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}))

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")

        return self.cleaned_data

    def save(self, user):
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user


class SendMailForm(forms.ModelForm):
    theme = forms.CharField(max_length=254, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Тема письма'}))

    class Meta:
        model = UserSending
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'style': 'resize: none;'
            })}
