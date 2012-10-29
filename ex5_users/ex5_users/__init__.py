from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.security import authenticated_userid
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid_zodbconn import get_connection

from .models import appmaker


def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())


# The 'get_user' method is registered below as a 'request_property'.
# This in effect makes available a 'user' attribute on the 'request'
# object.
def get_user(request, userid=None):
    # Ge the userid of the authenticated user, or return 'None' if no
    # user is authenticated.
    userid = userid or authenticated_userid(request)
    if userid is None:
        return None

    # Look up the user object and return it.
    try:
        return request.root[userid]
    except KeyError:
        return None


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(
        root_factory=root_factory,
        session_factory=UnencryptedCookieSessionFactoryConfig('itsaseekreet'),
        settings=settings,
        )

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan()

    config.set_request_property(get_user, 'user', reify=True)

    # Here, we register our authentication and authorization policies:
    authn_policy = AuthTktAuthenticationPolicy(secret='sosecret')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('deform_bootstrap')
    config.include('pyramid_deform')

    return config.make_wsgi_app()
