import os
from distutils.core import setup
from setuptools import find_packages

version = '0.2'
name = 'django-admin-csv'
dir = os.path.dirname(__file__)
readme = os.path.join(dir, 'README.rst')
github = 'https://github.com/bendavis78/'


setup(
    name=name,
    version=version,
    author='Ben Davis',
    keywords=['django', 'admin', 'csv'],
    author_email='bendavis78@gmail.com',
    url=github + name,
    download_url=github + name + '/tarball/' + version,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(),
    include_package_data=True,
    description='Adds a "download csv" option to your ModelAdmin.',
    long_description=open(readme).read()
)
