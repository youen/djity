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

def register(request,username,email,password1,password2):
    dajax = Dajax()
    if username == "":
        form =  RegistrationForm()
    else:
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
            msg = _(u'Your account is created !')
            messages.add_message(request, messages.INFO, unicode(msg) )
            dajax.script('location.reload()')
            return dajax.json()

    render = render_to_string('djity/portal/registration_form.html',{'form':form})
    dajax.assign('#register_dialog','innerHTML',render)
    dajax.script('register_dialog_post_assign()')
    return dajax.json()
dajax_register('register')

@check_perm_and_update_context()
def get_profile(request,context=None):
    target = context['JS_target']
    form =  ProfileForm()
    render = render_to_string('djity/portal/profile_form.html',{'form':form})
    target.user_profile('set_profile',render)

dajax_register('get_profile')


@check_perm_and_update_context()
def save_profile(request,password1,password2,context=None):
    target = context['JS_target']
    form = ProfileForm({
                    'password1':password1,
                    'password2':password2
                    })

    if form.is_valid():
        user = context['user']
        user.set_password(password1) 
        user.save()
        msg = unicode(_('Your password is changed'))
        target.message(msg)
        target.user_profile('close')

    for field in form.visible_fields():
        error = str(field.errors)
        if error != '':
            target.user_profile('error',field.auto_id,str(field.errors))
        
dajax_register('save_profile')


@check_perm_and_update_context()
def login(request, username, password, context):
    dajax = Dajax()
    user = authenticate(username=username,password=password)
    if user is None:
        dajax.script(u"login_dialog_error('%s')" % _("Authentication failed"))
        return dajax.json()
    if not user.is_active:
        dajax.script(u"login_dialog_error('%s')" % _("This account is disabled"))
        return dajax.json()
    django_login(request, user)
    msg = _(u'successfully connected')
    messages.add_message(request, messages.INFO, unicode(msg) )
    dajax.script("login_dialog_close()")
    dajax.script('location.reload()')
    return dajax.json()

dajax_register('login')
