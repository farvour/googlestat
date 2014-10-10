""" Main View Handler module.
"""
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from .models import DBSession, PingModel


@view_config(route_name='home', renderer='templates/main.jinja2')
def main_view(request):
    try:
        records = DBSession.query(PingModel).order_by(PingModel.date_added.desc()).limit(10).all()

    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    return {
        'project': 'googlestat',
        'records': records
    }


conn_err_msg = """\
I am having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_googlestat_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the application to
try it again.
"""
