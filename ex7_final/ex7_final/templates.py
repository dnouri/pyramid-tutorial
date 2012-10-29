"""This module provides a number of utility functions for use in templates.
"""

from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.location import lineage
from pyramid.security import has_permission


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

    def has_permission(self, permission):
        return has_permission(permission, self.request.context, self.request)
