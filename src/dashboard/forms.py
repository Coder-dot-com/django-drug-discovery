from django import forms
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(required=True,
        widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'id': 'current_password',
            'name': 'current_password',
            'title': "Enter your current password",
            'required': 'required',
            'placeholder':  "Enter your current password",
        }
    )
    )


    new_password = forms.CharField(required=True,
        widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'id': 'new_password',
            'name': 'new_password',
            'title': "Add a new password (min 12 chars)*",
            'required': 'required',
            'minlength': 12,
            'placeholder':  "Enter your new password here",

        }
    )
    )
    def clean_new_password(self):
        password = self.cleaned_data.get("new_password")
        if len(password) < 12:
            raise forms.ValidationError("Password isn't long enough")
        return password