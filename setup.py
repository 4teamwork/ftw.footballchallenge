from setuptools import setup, find_packages
import os

version = '1.0'
maintainer = 'Timon Tschanz'

tests_require = [
    'plone.app.testing',
    'plone.mocktestcase'
    '']

setup(name='ftw.footballchallenge',
      version=version,
      description="Some sort of Footballmanagergame based on Plone",
      # long_description=open('README.rst').read() + '\n' + \
      #   open(os.path.join('docs', 'HISTORY.txt')).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      maintainer=maintainer,
      keywords='Football Plone Python',
      author='4teamwork GmbH',
      author_email='info@4teamwork.ch',
      url='github.com/4teamwork/ftw.footballchallenge',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'SQLAlchemy',
          # -*- Extra requirements: -*-
      ],
      
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),      
      
      
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
