ex5_users
=========

In this part of the tutorial, we will add a 'User' model.  We'll also
implement authentication, and allow new users to register with our
site.


Install
-------

As usual, you should first install this example package::

  $ ../bin/python setup.py develop


User model
----------

A new 'User' model was added for you in 'ex5_users/models.py'.  Note
also that we add a default 'admin' user in the 'appmaker' function.


Authentication and authorization policy
---------------------------------------

Authentication (who is logged in) and authorization (what are they
allowed to do) are both pluggable in Pyramid.  For this example, we'll
use the 'AuthTktAuthenticationPolicy' and 'ACLAuthorizationPolicy'
modules provided by Pyramid itself.

We configure our Pyramid application with the authentication and
authorization policy in 'ex5_users/__init__.py'.

Notice also the new 'get_user' function in '__init__.py' and its
registration as a 'request property'.

Take a look at the 'ex5_users/templates/master.pt' template.  Code has
been added there to check for the existence of 'request.user' to
control display of login, register and logout links.


Logging in and out
------------------

Find the 'login.py' module, which contains views for logging in
('class Login') and logging out ('def logout').  Read the code and
comments and try to understand what's happening.

Then, open up your application in the browser, and click the "Sign in"
link at the top right corner to log in as the "admin" user (password:
"admin").

Further down in the 'login.py' module, you'll find some code for a
'Registration' view, which you will complete to allow users to
register with our application.  Add your code below "YOUR CODE HERE"
in the 'login.py' module.

After you have completed the code, you should be able to restart your
application and register as a new user.


Why implement this myself?
--------------------------

Pyramid itself doesn't come with login or logout views.  There is
however add-on packages that provide authentication and authorization
for you.  Notable examples are the Apex toolkit, substanced and Kotti.
