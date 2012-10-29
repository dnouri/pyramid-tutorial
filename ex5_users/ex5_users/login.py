from colander import Schema, SchemaNode, String
from deform.widget import PasswordWidget
from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget
from pyramid.security import remember
from pyramid.view import view_config
from pyramid_deform import FormView

from . import get_user


class LoginSchema(Schema):
    username = SchemaNode(String(), title=u"User name")
    password = SchemaNode(String(), title=u"Password", widget=PasswordWidget())


# Note how the 'login' view isn't registered for a particular
# 'context'.  This way, it's accessible for any item in our site.
# (However, we will only use it on the root.)
@view_config(name='login', renderer='templates/form.pt')
class Login(FormView):
    schema = LoginSchema()
    buttons = ('login',)
    title = u"Log in"

    def login_success(self, appstruct):
        user = get_user(self.request, appstruct['username'])
        if user is None:
            return self.bad_login()
        if not user.validate_password(appstruct['password']):
            return self.bad_login()

        # After we've validated the user's username and password, we
        # call 'pyramid.security.remember' to effectively set the
        # authentication cookie:
        headers = remember(self.request, user.__name__)
        self.request.session.flash(
            u"Welcome, {0}!".format(user.title), "success")
        return HTTPFound(location=self.request.application_url,
                         headers=headers)

    def bad_login(self):
        self.request.session.flash(
            u"Your username/password combination is incorrect.", "error")


# Logging out is simple.  Just call 'pyramid.security.forget' to
# remove the authentication cookie:
@view_config(name='logout')
def logout(request):
    headers = forget(request)
    request.session.flash(u"You have been logged out.")
    return HTTPFound(location=request.application_url, headers=headers)


# The 'RegistrationSchema' inherits from the LoginSchema.  This way,
# we inherit the 'username' and 'password' fields.
class RegistrationSchema(LoginSchema):
    fullname = SchemaNode(String(), title=u"Full name")
    email = SchemaNode(String(), title=u"Email")


# The 'Registration' view is similar to the 'FolderAdd' and 'PageAdd'.
# Upon success, it creates a new 'User' object.  It also logs in the
# user immediately.  You need to complete the 'register_success'
# method to this effect.
@view_config(name='register', renderer='templates/form.pt')
class Registration(FormView):
    schema = RegistrationSchema()
    buttons = ('register',)
    title = u"Register"

    def register_success(self, appstruct):
        username = appstruct.pop('username')
        user = get_user(self.request, username)
        if user is not None:
            self.request.session.flash(
                u"That username is already taken.", "error")
            return None

        # Complete the code here to
        # 1) create a user object (use 'user = User(...)')  (see models.py)
        # 2) add the user to the root object  (see models.py)
        # 3) use the 'remember' function (as above) to login the user
        # 4) display a success message

        # YOUR CODE HERE:
