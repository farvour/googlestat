""" Perform monitoring ping of site.
"""
import datetime
import requests
import transaction
from requests.packages.urllib3 import Timeout
from googlestat.models import DBSession, PingModel


class PingService(object):
    """ A service for pinging a site, and recording its data such as success, response time and code.
    """
    DEFAULT_TIMEOUT = 5.0
    """ How many seconds, maximum, to wait for a response? """

    def __init__(self, uri, max_timeout=DEFAULT_TIMEOUT):
        """ Init the class.

        :param uri: URL to hit.
        :type uri: str
        """
        self.uri = uri
        self.max_timeout = max_timeout

    @classmethod
    def ping_factory(cls, uri):
        """ Instantiate a ping object (mostly for background task).
        """
        ps = cls(uri=uri)
        ps.do_ping()

    def do_ping(self):
        """ Invoke requests to ask for a response.
        :return:
        """
        try:
            start_time = datetime.datetime.now()
            req = requests.get(self.uri, timeout=self.max_timeout)
            end_time = datetime.datetime.now()

            # Calculate the time delta.
            time_delta = end_time - start_time

            # Set code, time and success.
            response_code = req.status_code
            response_time = int(time_delta.microseconds)
            response_size = len(req.text)
            response_success = True

        except Timeout:
            # Set defaults of -1 and report that the response failed.
            response_code = -1
            response_time = -1
            response_size = 0
            response_success = False

        # Create data record.
        ping_record = PingModel()
        ping_record.site_url = self.uri
        ping_record.response_code = response_code
        ping_record.response_time = response_time
        ping_record.response_size = response_size
        ping_record.success = response_success
        ping_record.date_added = datetime.datetime.now()

        # Add to session.
        with transaction.manager:
            DBSession.add(ping_record)
            DBSession.flush()
