from django import template
from cab.models import Bookmark

def do_if_bookmarked(parser, token):
    
    bits = token.contents.split()
    
    # Sanity checking on args.
    if len(bits) != 3:
        raise template.TemplateSyntaxError("%s tag takes two arguments" % bits[0])
    
    # Parse.
    nodelist_true = parser.parse(('else', 'endif_bookmarked',))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif_bookmarked'))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()

    return IfBookmarkedNode(bits[1], bits[2], nodelist_true, nodelist_false)


class IfBookmarkedNode(template.Node):

    def __init__(self, user, snippet, nodelist_true, nodelist_false):
        self.user = template.Variable(user)
        self.snippet = template.Variable(snippet)
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):

        # Resolve the variables
        try:
            user = self.user.resolve(context)
            snippet = self.snippet.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        # Render the right if branch
        if Bookmark.objects.filter(user__pk=user.id,
                                   snippet__pk=snippet.id):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


register = template.Library()
register.tag('if_bookmarked', do_if_bookmarked)
