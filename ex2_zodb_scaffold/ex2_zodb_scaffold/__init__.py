from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
from .models import appmaker


# The 'root_factory' function is responsible for returning the
# 'application root object'.  This object can be thought of like the
# root in a file system, e.g. '/' on Unix.
def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())


# The 'main' function is the entry point into our application.  It is
# passed settings from the 'Paste Deploy configuration file'
# (e.g. 'development.ini') and is responsible for setting up the
# Pyramid application.
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=root_factory, settings=settings)

    # We add a 'static' view.  This allows us to access files in our
    # 'static' directory through the web.  Try accessing
    # http://localhost:6543/static/pylons.css
    config.add_static_view('static', 'static', cache_max_age=3600)

    # 'config.scan' looks for '@view_config' decorators and others
    # inside our project.
    config.scan()

    # Finally, return our configured Pyramid WSGI app.
    return config.make_wsgi_app()
