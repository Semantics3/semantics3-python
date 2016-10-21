import os
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = [
    'requests-oauthlib >= 0.4.0',
    'urltools == 0.3.2'
]
def read(fname):
   try:
      import pypandoc
      description = pypandoc.convert(fname, 'rst')
   except (IOError, ImportError):
      description = ''
   print(description)
   with open('README.rst','w') as f: f.write(description)
   return description

setup(
    name="semantics3",
    version="0.3.6",
    author="Shawn Tan, Abishek Bhat",
    author_email="abishek@semantics3.com",
    description=("Semantics3 Products API"),
    license="MIT",
    keywords="api ecommerce products",
    url="https://github.com/Semantics3/semantics3-python",
    packages=['semantics3'],
    long_description=read('README.md'),
    install_requires=install_requires,
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ]
)
