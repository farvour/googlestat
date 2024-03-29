import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid_scheduler',
    'pyramid_tm',
    'requests',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
]

setup(name='googlestat',
      version='0.1',
      description='googlestat - A simple connection and response status gatherer for google.com',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Thomas Farvour',
      author_email='tom@farvour.com',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='googlestat',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = googlestat:main
      [console_scripts]
      initialize_googlestat_db = googlestat.scripts.initializedb:main
      run_googlestat_ping = googlestat.scripts.ping:main
      """,)
