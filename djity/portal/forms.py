import re
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ProfileForm(forms.Form):
    password1 = forms.CharField(
            max_length=60,
            required=True,
            widget=forms.PasswordInput,
            )

    password2 = forms.CharField(
            max_length=60,
            required=True,
            widget=forms.PasswordInput,
            )

    def clean(self):
        cleaned_data = self.cleaned_data
        try :
            password1 = cleaned_data['password1']
            password2 = cleaned_data['password2']
            if password1 != password2:
                msg = _("Passwords don't match")
                self._errors['password1'] = self.error_class([msg])
                del cleaned_data['password1']
                del cleaned_data['password2']



        except KeyError:
            pass


        # Always return the full collection of cleaned data.
        return cleaned_data


class RegistrationForm(forms.Form):
    username = forms.CharField(
                    max_length=30,
                    required=True,
                    )

    email =  forms.EmailField(
                        max_length=30,
                        required=True
                 )
        
    password1 = forms.CharField(
                        max_length=60,
                        required=True,
                        widget=forms.PasswordInput,
                    )

    password2 = forms.CharField(
                        max_length=60,
                        required=True,
                        widget=forms.PasswordInput,
                    )



    def save(self):
        user = User(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                )

        user.set_password(self.cleaned_data['password1'])
        
        user.is_active = True
        user.save()
        return user




    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            username = cleaned_data['username']
            # check if username is a valid
            if check_username(username):
                msg = _('Username %s is not valid.'%username)
                self._errors['username'] = self.error_class([msg])
                del cleaned_data['username']
            #check if username doesn't exit
            else :
                unique_user = False
                try:
                    User.objects.get(username=username)
                except User.DoesNotExist:
                    unique_user = True
                
                if not unique_user :
                    msg = _('Username %s is not avaible.'%username)
                    self._errors['username'] = self.error_class([msg])
                    del cleaned_data['username']

        except KeyError:
            pass

        try :
            password1 = cleaned_data['password1']
            password2 = cleaned_data['password2']
            if password1 != password2:
                msg = _("Passwords don't match.")
                self._errors['password1'] = self.error_class([msg])
                del cleaned_data['password1']
                del cleaned_data['password2']



        except KeyError:
            pass


        # Always return the full collection of cleaned data.
        return cleaned_data

def check_username(username):
    """
    Check if username is valid
    """
    return re.compile('^[-|_|\w]+$').match(username)== None 

  
