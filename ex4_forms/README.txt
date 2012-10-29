ex4_forms
=========

In this part of the tutorial, we will add another model called 'Page',
so that then we're able to put pages into our folders.  We'll also
create HTML forms to be able to add, edit and delete folders and
pages.


Install
-------

As usual, you should first install this example package::

  $ ../bin/python setup.py develop

Notice how this will load a few extra packages.


Page model and view
-------------------

In 'models.py' you can now find another model: the 'Page'.  In
addition to the 'title' and 'description' attributes, this one also
has an HTML 'body'.

The 'page_view' in 'views.py' is pretty similar to our previous
'folder_view', except that it uses a different template to display
'Page' items.

Start up your server and click the 'about' link.  You're now looking
at a page.  Notice the HTML body.  Compare the output with what's in
the 'templates/page.pt' template.


Forms
-----

Further below in the 'views.py' file you'll find three classes with
which we implement the 'edit' and 'add' forms for the 'Folder'.  These
are:

- FolderSchema: This is a 'colander.Schema' that defines the fields
  that we're interested in.

- FolderAdd: The add form, which inherits from 'pyramid_deform.FormView'.

- FolderEdit: The edit form, which too inherits from
  'pyramid_deform.FormView'.

Try to read and understand the code and comments.  When you're done,
fire up the application and, on the root folder, click the 'Edit' link
to edit the 'title' and 'descrition' of your root folder.

Note that the 'Add page' doesn't work yet.  Also, clicking 'Edit'
while you're on the 'About' page doesn't work.  This is because we've
registered the 'edit' view only for 'Folder' items::

  @view_config(context=Folder, name='edit', renderer='templates/form.pt')

You should now implement edit and add forms for 'Page' items.  Add
your code below the "YOUR CODE HERE" line.

Implementation hint: You'll need to implement another three classes:
'PageSchema', 'PageAdd', and 'PageEdit'.  For the 'body' field, try to
use the 'deform.widget.RichTextWidget'.


Colander and Deform
-------------------

To implement the 'add' and 'edit' forms, we've been using the Colander
and Deform packages.  

- Colander allows us to define the structure of our data using a
  'Schema' class.

- Deform handles all the details of HTML forms for us.

- 'pyramid_deform' is a package that adds just a little bit of added
  convenience on top of Deform.  It provides the base class for our
  Pyramid views 'FolderView', 'FolderEdit', etc.

Extensive documentation exists online for both Colander and Deform:

- http://colander.readthedocs.org/en/latest/
- http://deform.readthedocs.org/en/latest/
