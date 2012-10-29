ex2_zodb_scaffold
=================

This example explains the various bits of code created by Pyramid's
'zodb' scaffold.

pcreate
-------

Pyramid's 'pcreate' tool creates a bunch of files for us that we can
use to quickly start off our Pyramid project.  To create a new Pyramid
project with the 'zodb' scaffold, you would normally run::

 $ bin/pcreate -s zodb myproject

'pcreate' comes with a few other scaffolds, we'll be using the 'zodb'
one.  For this example, the scaffold was already created for you (in
the same directory as this file).


ZODB
----

We choose to use the ZODB object database for this example and the
following ones.  With Pyramid, we're free to choose where to store our
data.  Pyramid itself is not tied to any particular database.  The
Pyramid Cookbook has details on how to use Pyramid with:

  - SQLAlchemy
  - CouchDB
  - MongoDB
  - ZODB

What is the ZODB?  From its website:

  The ZODB is a native object database, that stores your objects while
  allowing you to work with any paradigms that can be expressed in
  Python... there is no gap between the database and your program: no
  glue code to write, no mappings to configure.


ex2_zodb_scaffold is a distribution
-----------------------------------

The 'pcreate' command created a few files and directories for us.  In
particular, notice how the 'ex2_zodb_scaffold' directory, that you
find this file in, contains another directory with the same name
'ex2_zodb_scaffold/ex2_zodb_scaffold'.

The first 'ex2_zodb_scaffold' folder contains your Python distribution
(as they are found on the Python Package Index PyPI).

The second 'ex2_zodb_scaffold/ex2_zodb_scaffold' has our actual web
application code and static files in it.  We'll mostly deal with the
files in there.

But right now, we need to deal with installing our project into our
virtualenv.  To do this, change into the directory that contains this
file you're reading, and issue::

  $ ../bin/python setup.py develop
  running develop
  running egg_info
  ...
  Finished processing dependencies for ex2-zodb-scaffold==0.0

Notice that it went out to fetch a number of additional dependencies,
such as the 'ZODB' package, which are not included in the Pyramid
core, and therefore weren't installed in our virtualenv yet.


Run the ex2_zodb_scaffold example
---------------------------------

The 'ex2_zodb_scaffold' directory that 'pcreate' created for us is
runnable without any changes.  This is how you can start it up::

  $ ../bin/pserve development.ini
  2012-06-26 16:15:46,961 WARNI [ZODB.FileStorage][MainThread] Ignoring index for /home/daniel/docs/europy2012-pyramid-tutorial/ex2_zodb_scaffold/Data.fs
  Starting server in PID 11167.
  serving on http://0.0.0.0:6543

Visit http://localhost:6543 to see the default page.  Press Ctrl-C to
stop the application.

Take a look at the 'development.ini' file.  This is a 'Paste Deploy
configuration file'.  Its '[app:main]' section contains some
configuration parameters for your application, such as the database
URL.

The main entry point into our application is the 'def main' function
in the '__init__.py' module.  Find it.


Traversal
---------

In the previous example 'hello.py' from the first exercise, you
configured two routes to match your views with.  In this example, we
set up our views differently.  Concretely, we use 'Traversal' to map
URLs to objects, and we configure our views to display those objects.

Here's a bit of Python to illustrate Traversal:

  >>> def traverse(obj, path):
  ...     for segment in path.split('/'):
  ...         obj = obj[segment]
  ...     return obj

Consider this usage of the function::

  >>> root = {'files': {'accounting': {'2012-7': 'hello'}}}
  >>> traverse(root, path='files/accounting/2012-7')
  'hello'

This is essentially how Traversal works in Pyramid: the root object is
a dict-like object that returns its children upon dict access.

Let's take a closer look at the file 'ex2_zodb_scaffold/__init__.py',
where we define a 'root factory' that returns our application's root
object, and 'ex2_zodb_scaffold/models.py', where we define the class
of our application root, and create it.


pshell
------

The 'pshell' command allows us to interact with our application and
database through a Python shell.  To start up the shell, type::

  $ ../bin/pshell development.ini 
  Python 2.7.2+ (default, Oct  4 2011, 20:06:09) 
  [GCC 4.6.1] on linux2
  Type "help" for more information.

  Environment:
    app          The WSGI application.
    registry     Active Pyramid registry.
    request      Active request object.
    root         Root of the default resource tree.
    root_factory Default root factory used to create `root`.

  >>> root
  {}
  >>> type(root)
  <class 'ex2_zodb_scaffold.models.MyModel'>

Let us create a subfolder of root::

  >>> root.keys()
  []
  >>> from ex2_zodb_scaffold.models import MyModel
  >>> root['myfolder'] = MyModel()
  >>> root.keys()
  ['myfolder']

To save our changes, we have to commit the database transaction:

  >>> from transaction import commit
  >>> commit()

You can now enter Ctrl-D to exit the shell.  You should now be able to
visit http://localhost:6543/myfolder and not get a 404 error.


Other files in the project
--------------------------

- 'ex2_zodb_scaffold/views.py': the view function.  The 'my_view' view
  is configured as the 'default view' for any 'MyModel' object.

- 'ex2_zodb_scaffold/templates/mytemplate.pt': the template associated
  with the 'my_view' view.  The '${project}' inside the template
  renders to 'ex2_zodb_scaffold' because that's what our view returns.
  This is a 'Chameleon' template.

- 'ex2_zodb_scaffold/static/': contains static files that come with
  the project.  See the 'config.add_static_view' call in
  'ex2_zodb_scaffold/__init__.py'.

- 'Data.fs' contains the database.  It's created after the first run.
