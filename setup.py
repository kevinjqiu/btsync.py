from setuptools import setup, find_packages


version = '0.9.3'

setup(name='btsync.py',
      version=version,
      description="A Python API client for BitTorrent Sync",
      long_description=open('README.md').read(),
      classifiers=[],
      keywords='api',
      author='Kevin Jing Qiu',
      author_email='kevin.jing.qiu@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=open('requirements.txt').readlines(),
      entry_points={},
      )
