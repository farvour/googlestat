""" Application bootstrap.
"""
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from googlestat.models import DBSession, Base
from googlestat.services.ping import PingService


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Configure DB backend.
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    # Configure from PasteDeploy.
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('pyramid_scheduler')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()

    # Try and ping site while application runs, in the background.
    scheduler = config.registry.scheduler
    scheduler.add_interval_job(PingService.ping_factory, seconds=30, args=('http://www.google.com',))

    # Create the WSGI application.
    return config.make_wsgi_app()
