from django import template
from django.db.models import get_model
from coltrane.models import Entry


def do_latest_content(parser, token):

    # Argument sanity checking.
    bits = token.split_contents()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'get_latest_content' tag takes exactly 4 arguments")
    model_args = bits[1].split('.')
    if len(model_args) != 2:
        raise template.TemplateSyntaxError("First argument to 'get_latest_content' mush be an 'application name'.'model name' string")
    model = get_model(*model_args)
    if model is None:
        raise template.TemplateSyntaxError("'get_latest_content' tag got an invalid model: %s" % bits[1])
                                           
    return LatestContentNode(model, bits[2], bits[4])

class LatestContentNode(template.Node):

    def __init__(self, model, num, varname):
        self.model = model
        self.num = int(num)
        self.varname = varname

    # Puts the 5 latest entries in the context
    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''

register = template.Library()
register.tag('get_latest_content', do_latest_content)
