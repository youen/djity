from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def search_result(context, result):
    """
    Will render a search result for haystack by using the appropriate template for each model type
    """
    if result.app_label.startswith("djity_"):
        template_path = "%s/%s_search_result.html" % (result.app_label,result.model_name)
    else:
        template_path = "djity/%s/%s_search_result.html" % (result.app_label,result.model_name)
    return template.loader.render_to_string(template_path, {'result_url':result.object.djity_url(context)}, context)

