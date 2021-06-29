from setuptools import setup

setup(
    name='pyDismail',
    version='2',
    author='scrubjay55',
    packages=['pyDismail'],
    description='an API wrapper for yadim.dismail.de, a disposable mail provider',
    long_description=open('README.md').read(),
    install_requires=[
        "requests",
        "eml-parser"
    ],
)
