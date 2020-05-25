from setuptools import setup

setup(
name='pyDismail',
version='1',
author='scrubjay55',
packages=['pyDismail'],
description='a basic API wrapper for yadim.dismail.de, a disposable mail provider',
long_description=open('README.md').read(),
install_requires=[
   "requests",
   "beautifulsoup4",
   "lxml"
],
)