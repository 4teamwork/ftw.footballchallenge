from setuptools import setup, find_packages
import os

version = '1.0'
maintainer = 'Timon Tschanz'

tests_require = [
    'plone.app.testing',
    'plone.mocktestcase',
    'unittest2',
    ]

setup(name='ftw.footballchallenge',
      version=version,
      description="Some sort of Footballmanagergame based on Plone",
      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      maintainer=maintainer,
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      keywords='Football Plone Python',
      url='https://github.com/4teamwork/ftw.footballchallenge',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'SQLAlchemy',
        'ftw.datepicker',
        'ftw.tabbedview',
        'pyquery',
        'requests',
        'requests-cache',
        'setuptools',
        'z3c.saconfig',
        'zope.sqlalchemy<=0.7.7',
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
