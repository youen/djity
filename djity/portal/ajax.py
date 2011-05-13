# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
from dajax.core import Dajax
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _ 
from django.template.loader import render_to_string
from django.contrib import messages

from djity.portal.forms import RegistrationForm, ProfileForm
from djity.utils.decorators import djity_view

from dajaxice.core import dajaxice_functions
dajax_register = lambda name:dajaxice_functions.register_function('djity.portal.ajax',name)

@djity_view()
def logout(request,context=None):
    django_logout(request)
    dajax = Dajax()
    msg = _('You are now disconnected.')
    messages.add_message(request, messages.INFO, unicode(msg) )
    dajax.script('location.reload()')
    return dajax.json()
dajax_register('logout')

@djity_view()
def register(request,js_target,username,email,password1,password2,context=None):
    form = RegistrationForm({
                    'username':username,
                    'email':email,
                    'password1':password1,
                    'password2':password2
                })


    if form.is_valid():
        form.save()
        user = authenticate(username=username, password=password1)
        
        if user is not None:
            django_login(request,user)
            js_target.message(_('Your account is created ! your are connected as %s.'%username),post=True)
            js_target.message(_('We are creating your account... please wait.'))
            js_target.close()
            js_target.close()
            js_target.next()

    else:
        render = render_to_string('djity/portal/registration_form.html',{'form':form})
        js_target.set_form(render)
        
dajax_register('register')


@djity_view()
def get_register(request,js_target,context=None):
    form =  RegistrationForm()
    render = render_to_string('djity/portal/registration_form.html',{'form':form})
    js_target.set_form(render)

dajax_register('get_register')

@djity_view()
def get_profile(request,js_target,context=None):
    form =  ProfileForm()
    render = render_to_string('djity/portal/profile_form.html',{'form':form})
    js_target.set_profile(render)

dajax_register('get_profile')


@djity_view()
def save_profile(request,js_target,password1,password2,context=None):
    form = ProfileForm({
                    'password1':password1,
                    'password2':password2
                    })

    if form.is_valid():
        user = context['user']
        user.set_password(password1) 
        user.save()
        js_target.message(_('Your password has been changed.'))
        js_target.close()
    
    else:
        render = render_to_string('djity/portal/profile_form.html',{'form':form})
        js_target.set_profile(render)

        
dajax_register('save_profile')


@djity_view()
def login(request,js_target, username, password, context):
    user = authenticate(username=username,password=password)
    if user is None:
        js_target.message(_("Authentication failed."))
        return 
    if not user.is_active:
        js_target.message(_("This account is disabled."))
        return 
    django_login(request, user)
    js_target.message(_('You were successfully connected !'),post=True)
    js_target.message(_('Connecting... please wait.'))
    js_target.close()
    js_target.next()

dajax_register('login')
