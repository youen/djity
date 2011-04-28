# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.contrib.auth import logout as logout_response

from djity.project.decorators import check_perm_and_update_context 


@check_perm_and_update_context()
def overview(request,project='root',context=None):
    """
    Render the Homepage of a Djity site
    """

    # Return project overview template
    return render_to_response('djity/project/overview.html',context)

def logout(request):
    next_page = '/'
    if request.method == 'GET':
        next_page = request.GET.get('next_page',next_page)
    if request.method == 'POST':
        next_page = request.POST.get('next_page',next_page)
    
    response = logout_response(request, next_page=nex_page)
    response.delete_cookie('user_location')
    return response


@check_perm_and_update_context()
def login(request,context):
    context['next_page'] = request.GET['next']
    context['onload'] = "dj.widgets.login.open();"
    context['no_right_tabs'] = True
    return render_to_response('djity/project/account.html',context)
