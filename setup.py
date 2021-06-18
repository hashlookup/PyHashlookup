# -*- coding: utf-8 -*-
from setuptools import setup  # type: ignore


setup(
    name='pyhashlookup',
    version='1.0-dev',
    author='Raphaël Vinot',
    author_email='raphael.vinot@circl.lu',
    maintainer='Raphaël Vinot',
    url='https://github.com/CIRCL/pyhashlookup',
    description='Python client for CIRCL Hashlookup',
    packages=['pyhashlookup'],
    entry_points={"console_scripts": ["hashlookup = pyhashlookup:main"]},
    install_requires=['requests'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
        'Topic :: Internet',
    ]
)
