import os
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = [
    'oauth2 >= 1.5.211',
]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
setup(
    name="semantics3",
    version="0.0.1",
    author="Shawn Tan",
    author_email="shawn@semantics3.com",
    description=("Semantics3 Products API"),
    license="MIT",
    keywords="api ecommerce products",
    url="https://github.com/Semantics3/semantics3-python",
    packages=['semantics3'],
    long_description=read('README.rst'),
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ]
)
