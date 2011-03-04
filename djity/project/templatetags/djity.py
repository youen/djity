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

        return render_to_string("core/projects/tab.html",context)

@register.tag(name='instance_url')
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
        return context[self.var_name].djity_url(context)

from django.template.defaulttags import url, URLNode
import re
kwarg_re = re.compile(r"(?:(\w+)=)?(.+)")

@register.tag(name='djurl')
def do_djityurl(parser,token):
    bits = token.split_contents()
    print bits
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    viewname = bits[1]
    args = []
    kwargs = {}
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    # Backwards compatibility: check for the old comma separated format
    # {% url urlname arg1,arg2 %}
    # Initial check - that the first space separated bit has a comma in it
    if bits and ',' in bits[0]:
        check_old_format = True
        # In order to *really* be old format, there must be a comma
        # in *every* space separated bit, except the last.
        for bit in bits[1:-1]:
            if ',' not in bit:
                # No comma in this bit. Either the comma we found
                # in bit 1 was a false positive (e.g., comma in a string),
                # or there is a syntax problem with missing commas
                check_old_format = False
                break
    else:
        # No comma found - must be new format.
        check_old_format = False

    if check_old_format:
        # Confirm that this is old format by trying to parse the first
        # argument. An exception will be raised if the comma is
        # unexpected (i.e. outside of a static string).
        match = kwarg_re.match(bits[0])
        if match:
            value = match.groups()[1]
            try:
                parser.compile_filter(value)
            except TemplateSyntaxError:
                bits = ''.join(bits).split(',')

    # Now all the bits are parsed into new format,
    # process them as template vars
    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to url tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))

    return DjityURLNode(viewname, args, kwargs, asvar)

class DjityURLNode(template.Node):

    def __init__(self, view_name, args, kwargs, asvar):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self,context):
        from django.core.urlresolvers import reverse, NoReverseMatch
        if len(args) != 0 :
            args = [context['project_name']]
            kwargs = {}
        else:
            args = []
            kwargs = {'project_name': context['project_name'],'module_name':context['module_name']}

        args += [arg.resolve(context) for arg in self.args]
        kwargs.update(dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()]))


        # Try to look up the URL twice: once given the view name, and again
        # relative to what we guess is the "main" app. If they both fail,
        # re-raise the NoReverseMatch unless we're using the
        # {% url ... as var %} construct in which cause return nothing.
        url = ''
        try:
            url = reverse(self.view_name, args=args, kwargs=kwargs, current_app=context.current_app)
        except NoReverseMatch, e:
            if settings.SETTINGS_MODULE:
                project_name = settings.SETTINGS_MODULE.split('.')[0]
                try:
                    url = reverse(project_name + '.' + self.view_name,
                              args=args, kwargs=kwargs, current_app=context.current_app)
                except NoReverseMatch:
                    if self.asvar is None:
                        # Re-raise the original exception, not the one with
                        # the path relative to the project. This makes a
                        # better error message.
                        raise e
            else:
                if self.asvar is None:
                    raise e

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url



