from setuptools import setup

setup(
    name='pyDismail',
    version='2',
    project_urls={"Source": "https://github.com/scrubjay55/pyDismail.git"},
    url="https://github.com/scrubjay55/pyDismail.git",
    author='scrubjay55',
    license="APLv2",
    packages=['pyDismail'],
    description='an API wrapper for yadim.dismail.de, a disposable mail provider',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "requests",
        "eml-parser"
    ],
)
