"""This module provides a number of utility functions for use in templates.
"""

from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.location import lineage


# We use a 'BeforeRender' subscriber ('BeforeRender' is a Pyramid
# event), to add useful utility functions for use in our templates.
@subscriber(BeforeRender)
def add_global(event):
    event['utils'] = TemplateUtils(event['request'])


class TemplateUtils(object):
    def __init__(self, request):
        self.request = request

    # This method will be available as 'utils.breadcrumbs()' in any of
    # our templates.  You should call this method and use it to fix
    # the breadcrumbs bar.
    def breadcrumbs(self):
        # Notice the call to 'lineage', which internally uses the
        # '__parent__' attribute of our models to construct a list of
        # parent objects up to the root.  We reverse this list so that the
        # root object is at the first position:
        lin = list(lineage(self.request.context))
        lin.reverse()
        return lin
