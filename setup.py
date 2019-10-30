#!/usr/bin/env -S python3 -B -u

from sys import version_info
from setuptools import setup, find_packages

if version_info < (3, 5, 3):
    raise RuntimeError("aiopo requires Python 3.5.3+")

setup(
    name="aio-btalk",
    description='Async BeansTalk client (asyncio)',
    version="0.9.0",
    license='MIT',
    author='Vitold Sedyshev',
    author_email='vit1251@gmail.com',
    python_requires='>=3.5.3',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Development Status :: 4 - Beta',
#        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=["pyyaml"],
    zip_safe=True,
)
