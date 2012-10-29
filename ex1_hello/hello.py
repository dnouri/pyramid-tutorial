from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


# 'hello_world' is the function that's called when we open up
# http://localhost:8080/hello/bar in the browser.
# We call the 'hello_world' function a 'view'.  Views accept 'Request'
# objects and return 'Response' objects.
def hello_world(request):
    # The request.matchdict is a dictionary that has a 'name' entry,
    # which corresponds to the '{name}' part in our '/hello/{name}'
    # route below.
    return Response('Hello %(name)s!' % request.matchdict)


# Views may also return dictionaries:
def hello_json(request):
    return request.matchdict


if __name__ == '__main__':
    # Instantiate a Pyramid 'Configurator' object.  This one is used
    # to configure our views, and we'll use it ultimately to create
    # our WSGI application:
    config = Configurator()

    # This is the route configuration for our 'hello_world' view.
    # Note that the pattern has a variable part '{name}'.  Once our
    # view function is called, we can access the 'name' as
    # 'request.matchdict["name"]'.
    config.add_route(name='hello', pattern='/hello/{name}')

    # Next, we need to register our function as a view using the
    # 'hello' route we just defined:
    config.add_view(hello_world, route_name='hello')

    # Let's register another, slightly different route and associate
    # it with our second view: 'hello_json'.
    config.add_route(name='hello_json', pattern='/json/{name}')

    # Note that this time, we pass an additional 'renderer' argument
    # to 'config.add_view'.  This tells Pyramid to take the dictionary
    # that we return in our 'hello_json' function and turn it into a
    # JSON response.
    config.add_view(hello_json, route_name='hello_json', renderer='json')

    # We can now create our WSGI app and serve it using the standard
    # library 'wsgiref' server:
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    print("Server started at http://localhost:8080")
    server.serve_forever()
