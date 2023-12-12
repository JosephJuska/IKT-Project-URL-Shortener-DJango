from django import forms
from .models import UserModel
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['placeholder'] = 'Ex: username123...'
        self.fields['email'].widget.attrs['placeholder'] = 'Ex: email@email.com...'
        self.fields['password1'].widget.attrs['placeholder'] = 'Ex: password123...'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat your password...'

    def clean_email(self):
        email = self.cleaned_data['email']

        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')

        return email