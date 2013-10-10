from setuptools import setup, find_packages


version = '0.9.4'

setup(name='btsync.py',
      version=version,
      description="A Python API client for BitTorrent Sync",
      long_description=open('README.md').read(),
      classifiers=[],
      keywords='api',
      author='Kevin Jing Qiu',
      author_email='kevin.jing.qiu@gmail.com',
      url='https://github.com/kevinjqiu/btsync.py',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      data_files=[('.', ['requirements.txt', 'README.md', 'LICENSE'])],
      include_package_data=True,
      zip_safe=False,
      install_requires=open('requirements.txt').readlines(),
      entry_points={},
      )
