from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import User, Profile
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'gender', 'date_of_birth']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(max_length=35, min_length=3,
                                                    help_text="Enter your first name", widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
        self.fields['last_name'] = forms.CharField(max_length=35, min_length=3,
                                                   help_text="Enter your Last name", widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
        self.fields['date_of_birth'] = forms.DateField(
            required=True, widget=forms.DateInput(attrs={'type': 'date'}))
        self.fields['email'].widget.attrs.update(
            {'type': 'email', 'placeholder': 'example@example.com'})


class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Password'})


class CustomProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender',
                  'date_of_birth', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(
            max_length=35, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
        self.fields['last_name'] = forms.CharField(
            max_length=35, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
        self.fields['date_of_birth'] = forms.DateField(
            required=True, widget=forms.DateInput(attrs={'type': 'date'}))
        self.fields['email'].widget.attrs.update(
            {'type': 'email', 'placeholder': 'example@example.com', 'readonly': True})
        self.fields['username'] = forms.CharField(
            max_length=35, min_length=3, widget=forms.TextInput(attrs={'readonly': True}))
