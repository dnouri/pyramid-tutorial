from colander import Schema, SchemaNode, String
from deform.widget import PasswordWidget
from pyramid.httpexceptions import HTTPFound
from pyramid.security import Allow
from pyramid.security import forget
from pyramid.security import remember
from pyramid.view import view_config
from pyramid_deform import FormView

from . import get_user
from .models import User


class LoginSchema(Schema):
    username = SchemaNode(String(), title=u"User name")
    password = SchemaNode(String(), title=u"Password", widget=PasswordWidget())


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
        headers = remember(self.request, user.__name__)
        self.request.session.flash(
            u"Welcome, {0}!".format(user.title), "success")
        return HTTPFound(location=self.request.application_url,
                         headers=headers)

    def bad_login(self):
        self.request.session.flash(
            u"Your username/password combination is incorrect.", "error")


@view_config(name='logout')
def logout(request):
    headers = forget(request)
    request.session.flash(u"You have been logged out.")
    return HTTPFound(location=request.application_url, headers=headers)


class RegistrationSchema(LoginSchema):
    fullname = SchemaNode(String(), title=u"Full name")
    email = SchemaNode(String(), title=u"Email")


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

        user = self.request.root[username] = User(
            title=username,
            email=appstruct['email'],
            password=appstruct['password'],
            description=appstruct['fullname'],
            )

        user.__acl__ = [
            (Allow, user.__name__, 'edit'),
            (Allow, user.__name__, 'add'),
            (Allow, user.__name__, 'share'),
            ]

        headers = remember(self.request, user.__name__)
        self.request.session.flash(
            u"Your registration was successful!", "success")
        return HTTPFound(location=self.request.application_url,
                         headers=headers)
