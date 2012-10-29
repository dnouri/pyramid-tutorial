from colander import Schema, SchemaNode, String
from deform.widget import TextAreaWidget
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid_deform import FormView

from .models import Folder, Page


@view_config(context=Folder, renderer='templates/folder.pt')
def folder_view(context, request):
    return {}


# Note that our page is configued for 'Page' contexts, and that it's
# configured to use the 'templates/page.pt' template.
@view_config(context=Page, renderer='templates/page.pt')
def page_view(context, request):
    return {}


# Define the fields of the Folder form using a 'colander.Schema':
class FolderSchema(Schema):
    title = SchemaNode(String())
    description = SchemaNode(
        String(),
        widget=TextAreaWidget(rows=5),
        missing=u"",
        )


# This is the first class-based view that you've seen.  Pyramid
# supports classes for case where your view handler is best
# implemented as individual methods.

# This is the first time we specify a 'name' in the '@view_config()'.
# By default, the view's name is the empty string.  A view that's
# registered with an empty name is also called the 'default view'.
# The 'default view' is what we've been working with so far.

# The 'FolderAdd' view is registered using 'add-folder' as a name.  To
# access this view, you must append 'add-folder' to the URL path,
# e.g. http://localhost:6543/add-folder

# Here, we derive from 'pyramid_deform.FormView'.  In this class, we
# set a few attributes and add the 'save_success' method.

@view_config(context=Folder, name='add-folder', renderer='templates/form.pt')
class FolderAdd(FormView):
    schema = FolderSchema()  # the schema to use in this form
    buttons = ('save',)
    title = u"Add folder"  # used in the 'templates/form.pt' template

    # The 'save_success' method is called once the user clicked 'save'
    # and the data validated.
    def save_success(self, appstruct):
        # The context is always available as 'request.context'.
        context = self.request.context

        # Here is where we create our new folder and assign put it
        # into the context.
        new_folder = Folder(**appstruct)
        name = appstruct['title'].lower()
        context[name] = new_folder

        # Display a success message to the user.  (This requires a
        # SessionFactory be registered, see 'ex4_forms/__init__.py')
        self.request.session.flash(u"Your folder was added.", "success")

        # Finally, redirect the user to the 'default view' of the new
        # folder:
        return HTTPFound(location=self.request.resource_url(new_folder))


# The edit view is implemented and registered very similarly to the
# 'FolderAdd' view.  It is this view's job to allow editing an
# existing folder item.
@view_config(context=Folder, name='edit', renderer='templates/form.pt')
class FolderEdit(FormView):
    schema = FolderSchema()
    buttons = ('save',)
    title = u"Edit folder"

    # We use the 'appstruct' method to provide values from the context
    # to pre-fill the form.  The dict returned corresponds to the
    # fields in the 'FolderSchema'.
    def appstruct(self):
        context = self.request.context
        return {
            'title': context.title,
            'description': context.description,
            }

    def save_success(self, appstruct):
        context = self.request.context
        context.title = appstruct['title']
        context.description = appstruct['description']
        self.request.session.flash(u"Your changes have been saved.", "success")
        return HTTPFound(location=self.request.resource_url(context))


# To add a 'add' and 'edit' form for the 'Page' type, implement the
# following classes:

# class PageSchema(Schema):
#     ...
#
# @view_config(...)
# class PageAdd(FormView):
#     ...
#
# @view_config(...)
# class PageEdit(FormView):
#     ...

# YOUR CODE HERE:
