from setuptools import setup

from suche import __ver__

setup(name='suche',
      version=__ver__,
      description='Elasticsearch Export Framework',
      url='http://github.com/sachinvettithanam/suche',
      author='sachin philip mathew',
      author_email='me@imsach.in',
      license='MIT',
      packages=['suche'],
      install_requires=[
          "elasticsearch"
      ],
      zip_safe=False)
