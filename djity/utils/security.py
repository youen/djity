def sanitize(html):
    """
    sanitize html from submition
    http://blog.odonnell.nu/posts/html-comments/
    """
    
    from BeautifulSoup import BeautifulSoup
    import re
    # allow these tags. Other tags are removed, but their child elements remain
    whitelist = ['em', 'i', 'strong', 'u', 'a', 'b', 'p', 'br', 'code', 'pre', 'img' ]

    # allow only these attributes on these tags. No other tags are allowed any
    # attributes.
    attr_whitelist = {
                       'a':['href','title','hreflang'],
                       'img':['src'],
                     }

    # remove these tags, complete with contents.
    blacklist = [ 'script', 'style' ]

    attributes_with_urls = [ 'href', 'src' ]

    # BeautifulSoup is catching out-of-order and unclosed tags, so markup
    # can't leak out of comments and break the rest of the page.
    soup = BeautifulSoup(html)

    # now strip HTML we don't like.
    for tag in soup.findAll():
        if tag.name.lower() in blacklist:
            # blacklisted tags are removed in their entirety
            tag.extract()
        """
        elif tag.name.lower() in whitelist:
            # tag is allowed. Make sure all the attributes are allowed.
            for attr in tag.attrs:
                # allowed attributes are whitelisted per-tag
                if tag.name.lower() in attr_whitelist and \
                    attr[0].lower() in attr_whitelist[ tag.name.lower() ]:
                    # some attributes contain urls..
                    if attr[0].lower() in attributes_with_urls:
                        # ..make sure they're nice urls
                        if not re.match(r'(https?|ftp)://', attr[1].lower()):
                            tag.attrs.remove( attr )
                    # ok, then
                    pass
                else:
                    # not a whitelisted attribute. Remove it.
                    tag.attrs.remove( attr )
        else:
            # not a whitelisted tag. I'd like to remove it from the tree
            # and replace it with its children. But that's hard. It's much
            # easier to just replace it with an empty span tag.
            tag.name = "span"
            tag.attrs = []
"""

    # stringify back again
    safe_html = unicode(soup)

    # HTML comments can contain executable scripts, depending on the browser,
    # so we'll
    # be paranoid and just get rid of all of them
    # e.g. <!--[if lt IE 7]><script type="text/javascript">h4x0r();</script><!
    # [endif]-->
    # TODO - I rather suspect that this is the weakest part of the operation..
    safe_html = re.sub(r'<!--[.\n]*?-->','',safe_html)
    return safe_html

def db_table_exists(tables, cursor=None):
    """
    Inspired from here:
    https://gist.github.com/527113/307c2dec09ceeb647b8fa1d6d49591f3352cb034
    """
    try:
        if not cursor:
            from django.db import connection
            cursor = connection.cursor()
        if not cursor:
            raise Exception
        table_names = connection.introspection.get_table_list(cursor)
    except:
        raise Exception("unable to determine if the table '%s' exists" % table)
    else:
        for table in tables:
            if table in table_names:
                return True
        return False

