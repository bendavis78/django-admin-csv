from setuptools import setup, find_packages

version = '0.2'
name = 'django-admin-csv'

setup(
    name=name,
    version=version,
    test_suite='admin_csv.test',
    install_requires=[],
    packages=find_packages(),
    package_data={'admin_csv': ['*.html']},
    include_package_data=True,
    author='Ben Davis',
    keywords=['django', 'admin', 'csv'],
    author_email='bendavis78@gmail.com',
    license='MIT',
    url='https://github.com/bendavis78/' + name,
    download_url=('https://github.com/bendavis78/' + name + '/tarball/' +
                  version),
    long_description=open('README.rst').read(),
)
