from pyramid.view import view_config

# In this file, you should add a view called 'def folder_view' for our
# new 'Folder' model.  Use 'templates/folder.pt' as the template to
# render the view with.

# The 'context' object, the object that Pyramid traversed to before
# calling the view, is always implicitly availalbe in the template.
# Therefore, for this example, it will suffice to return an empty dict
# from your view.  The template will still be able to access
# '${context.title}' etc.

# Remember the previous example, where we returned a non-empty dict:

#     from .models import MyModel
#     @view_config(context=MyModel, renderer='templates/mytemplate.pt')
#     def my_view(context, request):
#         return {'project': 'ex3_templates'}


# YOUR CODE HERE:
