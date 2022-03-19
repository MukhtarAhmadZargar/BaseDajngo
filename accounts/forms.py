from accounts.models import *
import re
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

users = get_user_model()

alnum_re = re.compile(r"\w+$") 

regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)
    
class EmailValidationOnForgotPasswordForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("There is no user registered with the specified email address!")

        return email       