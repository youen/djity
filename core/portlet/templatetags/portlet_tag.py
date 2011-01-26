from django import template

register = template.Library()

@register.tag(name='portlet')
def do_portlet(parser, token):
    nodelist = parser.parse(('endportlet',))
    parser.delete_first_token()
    return PortletNode(nodelist)

class PortletNode(template.Node):
    def __init__(self, portlet):
        self.portlet = portlet

    def render(self, context):
        portlet_key = "portlet_%s"%self.portlet.render(context)
        return context[portlet_key].render(context)
