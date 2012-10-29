from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid_zodbconn import get_connection

from .models import appmaker


def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # The 'UnencryptedCookieSessionFactoryConfig' allows us to store
    # session data in a browser cookie.  This is required so that in
    # our views, we can call 'request.session.flash' to display
    # notifications to the user.
    config = Configurator(
        root_factory=root_factory,
        session_factory=UnencryptedCookieSessionFactoryConfig('itsaseekreet'),
        settings=settings,
        )

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan()

    config.include('deform_bootstrap')
    config.include('pyramid_deform')

    return config.make_wsgi_app()
