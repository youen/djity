from dajax.core import Dajax
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _ 
from django.template.loader import render_to_string
from django.contrib import messages

from djity.portal.forms import RegistrationForm, ProfileForm
from djity.project.decorators import check_perm_and_update_context

from dajaxice.core import dajaxice_functions
dajax_register = lambda name:dajaxice_functions.register_function('djity.portal.ajax',name)

@check_perm_and_update_context()
def logout(request,context=None):
    django_logout(request)
    dajax = Dajax()
    msg = _(u'You are now disconected')
    messages.add_message(request, messages.INFO, unicode(msg) )
    dajax.script('location.reload()')
    return dajax.json()
dajax_register('logout')

@check_perm_and_update_context()
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
            msg = unicode(_(u'Your account is created ! your are connected as %s'%username))
            messages.add_message(request, messages.INFO, unicode(msg) )
            msg = unicode(_(u'We are creating your account... please wait'))
            js_target.message(msg)
            js_target.close()
            js_target.reload()

    else:
        render = render_to_string('djity/portal/registration_form.html',{'form':form})
        js_target.set_form(render)
        
dajax_register('register')


@check_perm_and_update_context()
def get_register(request,js_target,context=None):
    form =  RegistrationForm()
    render = render_to_string('djity/portal/registration_form.html',{'form':form})
    js_target.set_form(render)

dajax_register('get_register')

@check_perm_and_update_context()
def get_profile(request,js_target,context=None):
    form =  ProfileForm()
    render = render_to_string('djity/portal/profile_form.html',{'form':form})
    js_target.set_profile(render)

dajax_register('get_profile')


@check_perm_and_update_context()
def save_profile(request,js_target,password1,password2,context=None):
    form = ProfileForm({
                    'password1':password1,
                    'password2':password2
                    })

    if form.is_valid():
        user = context['user']
        user.set_password(password1) 
        user.save()
        msg = unicode(_('Your password is changed'))
        js_target.message(msg)
        js_target.close()
    
    else:
        render = render_to_string('djity/portal/profile_form.html',{'form':form})
        js_target.set_profile(render)

        
dajax_register('save_profile')


@check_perm_and_update_context()
def login(request,js_target, username, password, context):
    user = authenticate(username=username,password=password)
    if user is None:
        js_target.message(unicode(_("Authentication failed")))
        return 
    if not user.is_active:
        js_target.message(unicode(_("This account is disabled")))
        return 
    django_login(request, user)
    msg = _(u'successfully connected')
    messages.add_message(request, messages.INFO, unicode(msg) )
    msg = _(u'connecting... please wait')
    js_target.message(unicode(msg))
    js_target.close()
    js_target.next()

dajax_register('login')
