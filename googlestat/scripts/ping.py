""" Perform monitoring ping of site.
"""
import os
import sys
from pyramid.paster import setup_logging, get_appsettings
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config
from googlestat.models import DBSession
from googlestat.services.ping import PingService


SITE_URL = 'http://www.google.com'
""" What URL to hit? """


def usage(argv):
    """ How to use this script, helper.

    :param argv: Arguments to pass into application.
    """
    cmd = os.path.basename(argv[0])

    print('usage: %s <config_uri> [var=value]\n(example: "%s development.ini")' % (cmd, cmd))

    sys.exit(1)


def main(argv=sys.argv):
    """ Invoke the ping and collect statistics into DB.

    :param argv: Arguments to pass into application.
    """
    if len(argv) < 2:
        usage(argv)

    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')

    DBSession.configure(bind=engine)

    # Instantiate a ping service.
    ps = PingService(uri=SITE_URL)
    ps.do_ping()

