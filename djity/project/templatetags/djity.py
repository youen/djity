from django.template.loader import render_to_string
from django import template

register = template.Library()

@register.tag(name='tab')
def do_tab(parser, token):
    nodelist = parser.parse(('endtab',))
    parser.delete_first_token()
    return TabNode(nodelist)

class TabNode(template.Node):
    def __init__(self, module):
        self.module = module

    def render(self, context):
        module = self.module.render(context)
        tab_context = {
            "tab_display":context["%s_tab_display"%module],
            "tab_url":context["%s_tab_url"%module],
            "tab_id":module,
        }
        context.update(tab_context)

        return render_to_string("djity/project/tab.html",context)

@register.tag(name='djiurl')
def do_djiurl(parser,token):
     try:
         # split_contents() knows not to split quoted strings.
         tag_name, var_name = token.split_contents()
     except ValueError:
         raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
     return DjityInstanceURLNode(var_name)

class DjityInstanceURLNode(template.Node):
    def __init__(self,var_name):
        self.var_name = var_name

    def render(self,context):
        return context[self.var_name].djity_url(context=context)


