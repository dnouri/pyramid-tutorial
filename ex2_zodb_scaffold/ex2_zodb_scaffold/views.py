from pyramid.view import view_config
from .models import MyModel


# Unlike in the 'hello.py' example, we now use a decorator to register
# our view.

# Note that with Traversal, there is no route associated with the
# view.  We use a 'context' argument instead.  Here, we tell Pyramid
# to use this view whenever it traverses to a 'MyModel' object.  We
# get passed as 'context' into our function the object that Pyramid
# traversed to.  For the URL path '/', this will be the root object.

# Note also that, instead of returning a 'Response' from our view, we
# return a dictionary.  Pyramid passes this dictionary of variables to
# the template in 'templates/mytemplate.pt', which happens to be our
# view's 'renderer'.
@view_config(context=MyModel, renderer='templates/mytemplate.pt')
def my_view(context, request):
    return {'project': 'ex2_zodb_scaffold'}
