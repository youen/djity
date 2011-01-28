import Image,os

from django.conf import settings
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseNotAllowed
from django.shortcuts import render_to_response

from djity.portal.models import SiteRoot
from djity.project.models import Project,is_active,has_perm
from djity.project.decorators import check_perm_and_update_context
from djity.style.models import CSS

def update_css_context(css_context,get):
    for style in css_context:
        if style in get:
            css_context[style] = get[style]

@check_perm_and_update_context()
def css(request,template,context=None):
    """
    #Render the CSS stylesheet for a project
    """
    # either use css values passed in a dictionary as parameter of fetch it in
    # the database
    project = context['project']
    css_context = project.css.get_context()
    if request.method == 'GET':
        update_css_context(css_context,request.GET)

    # Create context for template rendering
    context.update(css_context)

    httpresponse = render_to_response(template,context)
    httpresponse['Content-Type']="text/css"
    return httpresponse

@check_perm_and_update_context()
def themeroller(request,context=None):
    project = context['project']
    css = project.css

    css_context = css.get_context()

    edit_style_content = []
    for group,items in settings.EDIT_STYLE_ORDER:
        content_items = []
        for item in items:
            content_items.append((item[0],item[1],css_context[item[1]],item[1].split('_')[-1]))
        edit_style_content.append((group,content_items))

    context['edit_style_content'] = edit_style_content
    context['textures'] = css_context['textures']

    return render_to_response("core/style/themeroller.html",context)

def texture(request,project_name): 
    try:
        get = request.GET
        filename = get['filename'].split('/')[-1]
        bg_color = get['bg_color'].split('/')[-1]
        percent = int(get['percent'])/100.0
    except:
        return HttpResponseNotFound()

    # check cache for previously computed image
    cache = "%s/cache/%s_%s_%s" % (settings.TEXTURES_DIR,bg_color,percent,filename)
    if os.path.isfile(cache):
        response = HttpResponse(mimetype="image/png")
        cache = open(cache,'r')
        response.write(cache.read())
        cache.close()
        return response

    try:
        path = settings.TEXTURES_DIR+'/'+filename
        im = Image.open(path)
    except:
        return HttpResponseNotFound()

    transparent = Image.new('RGBA',im.size,(0,0,0,0))
    blended = Image.blend(transparent,im,percent)
    bg = Image.new('RGBA',im.size,bg_color)
    bg.paste(blended,None,blended)
    response = HttpResponse(mimetype="image/png")
    bg.save(cache)
    bg.save(response,'PNG')
    return response

def icons(request,project_name):
    try:
        get = request.GET
        color = get['color'].split('/')[-1]
    except:
        return HttpResponseNotFound()

    cache = "%s/cache/%s_icons.png" % (settings.ICONS_DIR,color)
    if os.path.isfile(cache):
        response = HttpResponse(mimetype="image/png")
        cache = open(cache,'r')
        response.write(cache.read())
        cache.close()
        return response

    try:
        im = Image.open("%s/icons_mask.png" % settings.ICONS_DIR)
    except:
        return HttpResponseNotFound()

    bg = Image.new('RGB',im.size,color)
    tr = Image.new('RGBA',im.size,(0,0,0,0))
    result = Image.composite(bg,tr,im)
    response = HttpResponse(mimetype="image/png")
    result.save(cache)
    result.save(response,'PNG')
    return response

"""
@check_perm_and_update_context()
def project_css(request,context=None):
    #Render the CSS stylesheet for a project

    # either use css values passed in a dictionary as parameter of fetch it in
    # the database
    project = context['project']
    css_context = project.css.get_context()
    if request.method == 'GET':
        update_css_context(css_context,request.GET)

    # Create context for template rendering
    context.update(css_context)

    httpresponse = render_to_response('core/style/project.css',context)
    httpresponse['Content-Type']="text/css"
    return httpresponse

@check_perm_and_update_context()
def ui_css(request,context=None):
    #Render the CSS stylesheet for a project
    
    # either use css values passed in a dictionary as parameter of fetch it in
    # the database
    project = context['project']
    css_context = project.ui_css.get_context()
    if request.method == 'GET':
        update_css_context(css_context,request.GET)

    # Create context for template rendering
    context.update(css_context)

    httpresponse = render_to_response('core/style/jquery-ui.css',context)
    httpresponse['Content-Type']="text/css"
    return httpresponse
"""
# module_css is not used yet
#def module_css(request,module_name='overview'):
#    """
#    Render the CSS stylesheet for a module in a project
#    """
#    # Try to fetch current CSS
#    try:
#        project = Project.objects.get(name=project)
#        module = Module.objects.get(project=project,module_name=module)
#        css = module.css
#    except:
#        return HttpResponseNotFound()
#
#    if not has_perm(project,request.user,'view'):
#        return HttpResponseNotAllowed([])
#
#    # Create context for template rendering
#    context = css.get_context()
#
#    httpresponse = render_to_response("core/style/%s.css"%module_name,context)
#    httpresponse['Content-Type']="text/css"
#    return httpresponse

