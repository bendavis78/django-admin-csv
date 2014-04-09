from distutils.core import setup

setup(
    name='django-admin-csv',
    version='0.1-dev',
    test_suite='admin_csv.test',
    moddules=['admin_csv.py'],
    install_requires=[],
    package_data={'admin_csv': ['*.html']},
    include_package_data=True,
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.rst').read(),
)
