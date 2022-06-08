from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    description = f.read()

requires = ['requests==2.25.1']

setup(
    name='pyspapi',
    version='1.0.2',
    description='API wrapper for SP servers written in Python',
    long_description=description,
    long_description_content_type='text/markdown',
    author='deesiigneer',
    author_email='xdeesiigneerx@gmail.com',
    packages=['spapi'],
    install_requires=requires,
)
