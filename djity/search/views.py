from django.conf import settings

from haystack.views import basic_search
from haystack.query import SearchQuerySet

from djity.utils.decorators import djity_view
from djity.utils.context import DjityContext

@djity_view(perm='view')
def project_search(request,context=None):
    """
    Override haystack basic_view for customization.
    """
    sqs = SearchQuerySet().narrow("project:%s"% context['project'].id).narrow("status:%s" % settings.LOWER_VISIBLE_STATUS[context['role']])
    #for hidden_status in settings.HIDDEN_STATUSES[context['role']]:
    #    sqs = sqs.exclude(status=hidden_status)
    print sqs
    return basic_search(request, template='djity/search/search.html', searchqueryset=sqs, extra_context=context, context_class=DjityContext)
