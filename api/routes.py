
from views.visited_links import VisitedLinks 
from views.visited_domains import VisitedDomains

ROUTS = {
    '/visited_links/': {
        'method': 'POST',
        'web_view': VisitedLinks,
        'name': 'VisitedLinks'
    },
    '/visited_domains/': {
        'method': 'GET',
        'web_view': VisitedDomains,
        'name': 'VisitedDomains'
    }
}


def setup_routes(app):
    for route, route_args in ROUTS.items():
        app.router.add_route(
            route_args['method'],
            route,
            route_args['web_view'],
            name=route_args['name'],
        )
