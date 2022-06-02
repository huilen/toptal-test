from django.contrib.auth import password_validation
from django.forms import CharField, ModelForm, PasswordInput

from .models import User


class UserCreationForm(ModelForm):
    password = CharField(
        label="Password",
        strip=False,
        widget=PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ["email", "name"]

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class SettingsForm(ModelForm):
    password = CharField(
        label="Password",
        strip=False,
        required=False,
        widget=PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ["email", "name", "bio", "image"]

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
