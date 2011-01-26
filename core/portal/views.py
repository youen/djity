from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import login ,authenticate
from django.utils.translation import get_language
from django.template import RequestContext
from djity.core.portal.forms import RegistrationForm, ProfileForm
from djity.core.portal.models import UserProfile
from djity.core.project.decorators import check_perm_and_update_context 

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
             
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/'+ get_language()[:2])

    else:
        form = RegistrationForm() # An unbound form
    
    return render_to_response('core/portal/registration_page.html',{'form':form}, context_instance=RequestContext(request))

def profile(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            password1 = request.POST['password1']
            
            user =  request.user
            user.set_password(password1)
            user.save()

            return HttpResponseRedirect('/'+ get_language()[:2])
    else :
        form = ProfileForm()


    return render_to_response('core/portal/profile_page.html', {'form':form},context_instance=RequestContext(request))



        

