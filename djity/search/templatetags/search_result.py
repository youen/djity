from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def search_result(context, result):
    """
    Will render a search result for haystack by using the appropriate template for each model type
    """
    return template.loader.render_to_string("djity/%s/%s_search_result.html"  % (result.app_label,result.model_name), {'result_url':result.object.djity_url(context)}, context)

