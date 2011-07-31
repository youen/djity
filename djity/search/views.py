from haystack.views import basic_search
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from djity.utils.decorators import djity_view
from djity.utils.context import DjityContext

@djity_view(perm='view')
def project_search(request,context=None):
    """
    Override haystack basic_view for customization
    """    
    sqs = SearchQuerySet().filter(project=context['project'])
    #sqs = SearchQuerySet()
    return basic_search(request, template='djity/search/search.html', searchqueryset=sqs, extra_context=context, context_class=DjityContext)
