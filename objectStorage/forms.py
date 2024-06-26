# # forms.py
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
#
# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(max_length=100, required=True, help_text='Required. Enter a valid email address.')
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')
