ex3_templates
=============

In this step, we will implement our own first model, a 'Folder'.

We will also split up our template, so that elements such as logo and
navigation that appear in all our HTML pages, are separated out into a
'master template'.


Install
-------

Just like with the 'ex2_zodb_scaffold' example, you'll need to setup
the 'ex3_templates' project to be able to run it.  Maybe like this::

  $ ../bin/python setup.py develop

After starting the server you should try to access
http://localhost:6543 again::

  $ ../bin/pserve development.ini
  Starting server in PID ...
  serving on http://0.0.0.0:6543

You'll see a "404 Not Found" page.  This is expected.


The Folder model
----------------

Visit the file 'models.py' and notice that we have replaced the
'MyModel' class from the previous example with a 'Folder' model class.
Try to read and understand the code.


A view for our Folder
---------------------

In the 'views.py' file, we'll need to create a view for our 'Folder'
model.  To do this, we'll have to adapt the code from the previous
example.

Open the 'views.py' file and read the comments.  Then implement the
view function below where it says "YOUR CODE HERE:".

After implementing the 'folder_view' view, you should restart your
server and point your browser to http://localhost:6543 again.  This
time, you should see a proper response instead of the 404.


Master template
---------------

Notice that the look and feel was changed to use Twitter Bootstrap.
First, take a look at the new contents of our 'static' folder.  In
particular, notice how there's now a copy of the bootstrap resources
and a copy of jQuery included.

Next, take a look at the 'templates/' folder.  You'll notice that
there's now two templates.  The 'master.pt' template is our HTML
framework that provides a consistent look and feel for our application
and includes all the resources and JS file.  The 'folder.pt' template
is only concerned about displaying the relevant items of a folder.

Open to 'folder.pt' template and notice how the '<html>' root tag has
a funny 'metal:use-macro' attribute.  This and the 'metal:fill-slot'
attribute in the '<div>' below is how we connect the 'folder.pt'
template with the 'master.pt' template.

If you want to find out more about Chameleon and templates, there's
some documentation here:
http://chameleon.repoze.org/docs/latest/reference.html#macros-metal

Notice how, in both templates, we have access to the 'context' object,
which is the object that we've traversed to, and we're looking at.

Take a look at how we make a loop over all our context's 'values'.  We
use 'tal:repeat' to create a list with links to the item's children.

To be able to see this construct in action, we'll again use the
'pshell' command to add two more folders to our tree::

    $ ../bin/pshell development.ini 
    ...
    >>> from ex3_templates.models import Folder
    >>> hello = root["hello"] = Folder("Hello folder")
    >>> hello["florence"] = Folder("Florence", description="Quite beautiful")
    >>> from transaction import commit
    >>> commit()

Now start up the server again, and use the links to navigate through
your tree.


Template globals and breadcrumbs
--------------------------------

Notice how there's a broken breadcrumbs bar above the content area.
Let's fix this.  But first, take a look at the new 'templates.py'
module.  Notice the 'add_global' function, which is used to make
available handy utility functions for use in our templates.

Now that you've learned that you can use 'utils.breadcrumbs()' in your
template to get a list of objects, try to use it to construct the
breadcrumbs bar dynamically.  If you need help with the 'tal:repeat'
syntax, try to look at the example in 'templates/folder.pt'.

You should now fix the breadcrumbs code in the 'master.pt' template.
Look for "YOUR CODE HERE".

Implementation hint: To be able to mark the current object with the
'active' class, it will be maybe useful to first iterate over
'breadcrumbs[:-1]' and then display 'breadcrumbs[-1]' in a separate
'<li>' tag.  If you've worked with Chameleon templates before, you
might be able to use a condition instead inside the same '<li>'
element instead.
