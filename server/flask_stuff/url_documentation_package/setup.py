from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
setup( name='URLdocs',

       version='0.1',
       description='A module that allows you to document python functions, and generate HTML output of that documentation',
       py_modules=['url_documentation'])


