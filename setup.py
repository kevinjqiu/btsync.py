from setuptools import setup, find_packages
import sys, os

version = '0.9'

setup(name='btsync.py',
      version=version,
      description="A Python API client for BitTorrent Sync",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='api',
      author='Kevin Jing Qiu',
      author_email='kevin.jing.qiu@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
