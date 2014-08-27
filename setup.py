from setuptools import setup, find_packages


version = '0.9.8'

setup(name='btsync.py',
      version=version,
      description="A Python API client for BitTorrent Sync",
      long_description=open('README.rst').read(),
      classifiers=[
          'Intended Audience :: Developers',
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
      ],
      keywords='api',
      author='Kevin Jing Qiu',
      author_email='kevin.jing.qiu@gmail.com',
      url='https://github.com/kevinjqiu/btsync.py',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      data_files=[('.', ['requirements.txt', 'README.rst', 'LICENSE'])],
      include_package_data=True,
      zip_safe=False,
      install_requires=open('requirements.txt').readlines(),
      entry_points={},
      )
