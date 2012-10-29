ex6_security
============

In the final part of this tutorial, you will learn about security in
Pyramid.  Concretely, you will guard your add and edit views with
permissions, so that anonymous users can no longer edit any content.
You will learn how to make use of Access Control Lists to allow users
to edit content in their respective user folders.


Install
-------

As usual, you should first install this example package::

  $ ../bin/python setup.py develop


Access Control Lists
--------------------

In the 'ex6_security/models.py' module, in the 'appmaker' function,
we've added a bit of code to set an Access Control List on the root
object.  This is how we do it::

  app_root.__acl__ = [
      (Allow, 'admin', ALL_PERMISSIONS),
      ]

Note how the '__acl__' attribute contains a list of 3-tuples.  Each
one of these tuples constitutes an "Access Control Entry" (or ACE).

We added a single ACE to our root object, which basically reads as:
"Grant the admin user all permission on this object and below."

ACLs are inherited down the object graph, that is, not only does the
'admin' user have 'ALL_PERMISSION' on the root object, but also on all
objects below root.  Which effectively means that 'admin' has all
permissions everywhere.


Guarding views with permissions
-------------------------------

In 'ex6_security/views.py' you'll find that all our add and edit views
are now configured with an additional 'permission' parameter.  We're
now guarding the add views with the 'add' permission and the edit
views with the 'edit' permission.

Fire up the application, and try to access the add and edit forms
first as the 'admin' user, and then as a newly registered user.  You
will find that accessing the add and edit forms with a normal user
results in "403 Forbidden" response.


The 'has_permission' function
-----------------------------

Pyramid comes with the 'pyramid.security.has_permission' function,
which allows you to check whether the logged in user has a certain
permission.

As an exercise, you should a 'has_permission' method to the
'TemplateUtils' class in 'ex6_security/templates.py'.  You should then
use that 'has_permission' method to display the add and edit links
only to those users that have the respective permission.

Once you're done, you should see that only the admin user sees the add
and edit links at this point.  Notice how normal users don't see the
links anywhere, not even in their own folders.  We'll fix this next.


Allowing users to edit their own data
-------------------------------------

Next, you should add code in the 'Registration' view in
'ex6_security/login.py' to allow users to edit and add pages and
folders in their own user folders.  Look for "YOUR CODE HERE" in the
'login.py' module, and complete the code.


Allowing users to collaborate on content
----------------------------------------

In this part of the exercise you should grant more than one user the
'add' and 'edit' permissions in a certain folder.  This will allow
users to collaboratively work on the content in that folder.

To start out this exercise, first experiment a little with the Pyramid
shell.  Say you registered a new user called 'daniel' in your site,
then, to access that user's folder in the 'pshell', you would enter
the following code::

  $ ../bin/pshell development.ini 
  ...
  Environment:
    app          The WSGI application.
    registry     Active Pyramid registry.
    request      Active request object.
    root         Root of the default resource tree.
    root_factory Default root factory used to create `root`.

  >>> root['daniel'].__acl__
  [('Allow', 'daniel', 'edit'), ('Allow', 'daniel', 'add'), ('Allow', 'daniel', 'share')]

Add another entry to this ACL to allow user 'alice' to add and edit
content in Daniel's folder (but not 'share').  For this, make sure you
assign to the '__acl__' attribute and not merely append to the list.

Don't forget to commit the transaction when you're done::

  >>> from transaction import commit
  >>> commit()

Once done, you should register the 'alice' user in your site and
confirm that she can indeed add and edit content in Daniel's folder.

You should now continue to add a 'Share' link right below the 'Edit'
link in the 'master.pt' template.  After adding the link, add another
view in 'ex6_security/views.py', one that allows users to grant 'edit'
and 'add' to the folder or page they're looking at to other users.
(Similar to the shell example above, where you added 'add' and 'edit'
for user 'alice' in Daniel's home folder.)


A separate User view and 'following' users
------------------------------------------

Note that, until now, we've been using the 'folder_view' for both
'Folder' and 'User' items.  Create a view and a template for the
'User' object in order to display additional information about the
user, like the user's email address.

In that view, add a 'follow' button for authenticated users to allow
your users to connect with each other.  Remember that our User object
already has an attribute 'followers', which is a list of User objects.
You should implement a 'follow' view to allow the logged in user to
add themselves to the list of followers.

After you have completed the 'follow' view, add another 'unfollow'
view so that users can stop following.
