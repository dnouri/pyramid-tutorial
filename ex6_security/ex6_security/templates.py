"""This module provides a number of utility functions for use in templates.
"""

from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.location import lineage


@subscriber(BeforeRender)
def add_global(event):
    event['utils'] = TemplateUtils(event['request'])


class TemplateUtils(object):
    def __init__(self, request):
        self.request = request

    def breadcrumbs(self):
        lin = list(lineage(self.request.context))
        lin.reverse()
        return lin

    # Add a 'has_permission' method here to make permission checking
    # available to your template.

    # Once you have implemented this method, you can then use the
    # 'has_permission' method in your template to conditionally
    # display the add and edit links, maybe like so:

    #   <li tal:condition="utils.has_permission('edit')">...</li>

    # Note that the arguments to 'pyramid.security.has_permission' are
    # '(permission, context, request)'.

    # YOUR CODE HERE:
