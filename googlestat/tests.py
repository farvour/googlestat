""" Google Stat Tests.
"""
import unittest
import transaction
from pyramid import testing
from .models import DBSession


class TestMyViewSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

        from sqlalchemy import create_engine

        engine = create_engine('sqlite://')

        from .models import Base, PingModel

        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

        with transaction.manager:
            model = PingModel()
            model.site_url = 'http://www.google.com'
            model.success = True
            model.response_code = 200
            model.response_time = 15000

            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_passing_view(self):
        from .views import main_view

        request = testing.DummyRequest()

        info = main_view(request)

        # self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'googlestat')


class TestMyViewFailureCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

        from sqlalchemy import create_engine

        engine = create_engine('sqlite://')

        from .models import Base, PingModel

        DBSession.configure(bind=engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_failing_view(self):
        from .views import main_view

        request = testing.DummyRequest()

        info = main_view(request)

        self.assertEqual(info.status_int, 500)
