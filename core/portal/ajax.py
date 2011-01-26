from dajax.core import Dajax
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _ 
from django.template.loader import render_to_string
from django.contrib import messages

from djity.core.portal.forms import RegistrationForm, ProfileForm
from djity.core.project.decorators import check_perm_and_update_context

from dajaxice.core import dajaxice_functions
dajax_register = lambda name:dajaxice_functions.register_function('djity.core.portal.ajax',name)

def logout(request):
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

    render = render_to_string('core/portal/registration_form.html',{'form':form})
    dajax.assign('#register_dialog','innerHTML',render)
    dajax.script('register_dialog_post_assign()')
    return dajax.json()
dajax_register('register')

@check_perm_and_update_context()
def profile(request,password1,password2,context=None):
    dajax = Dajax()
    if password1 == "":
        form =  ProfileForm()
    else:
        form = ProfileForm({
                    'password1':password1,
                    'password2':password2
                    })

    if form.is_valid():
        user = context['user']
        user.set_password(password1) 
        user.save()
        msg = unicode(_('Your password is changed'))
        dajax.script("$('#profile_dialog').dialog('close')")
        dajax.script(u'message("%s")'%msg)
        return dajax.json()

    render = render_to_string('core/portal/profile_form.html',{'form':form})
    dajax.assign('#profile_dialog','innerHTML',render)
    dajax.script('profile_dialog_post_assign()')
    return dajax.json()   
        
dajax_register('profile')




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
