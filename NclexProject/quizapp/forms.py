from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div
from django.contrib.auth import authenticate

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'p-4 bg-light shadow rounded'
        self.helper.label_class = 'form-label'
        self.helper.field_class = 'form-control'
        self.helper.layout = Layout(
            Div(
                Field('name', placeholder='Your Name'),
                Field('password1'),
                Field('password2'),
                Submit('submit', 'Register', css_class='btn btn-primary w-100 mt-3'),
                css_class="form-group"
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password1"])  # Hash the password
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        label='Password'
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'p-4 bg-light shadow rounded'
        self.helper.label_class = 'form-label'
        self.helper.field_class = 'form-control'
        self.helper.layout = Layout(
            Div(
                Field('username'),
                Field('password'),
                Submit('submit', 'Login', css_class='btn btn-primary w-100 mt-3'),
                css_class="form-group"
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        password = cleaned_data.get('password')

        if name and password:
            user = authenticate(username=name, password=password)
            if not user :
                raise forms.ValidationError("Username or password is incorrect.")
            self.user = user  # Save the authenticated user for use in the view
        return cleaned_data