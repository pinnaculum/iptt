from setuptools import setup
from setuptools import find_packages

from iptt import __version__


def reqs_parse(path):
    with open(path) as f:
        return f.read().splitlines()


install_reqs = reqs_parse('requirements.txt')
found_packages = find_packages(exclude=['tests', 'tests.*'])


with open('README.rst', 'r') as fh:
    long_description = fh.read()


setup(
    name='iptt',
    version=__version__,
    license='DEV-NULL',
    author='cipres',
    author_email='galacteek@protonmail.com',
    url='https://gitlab.com/galacteek/iptt/iptt',
    description='InterPlanetary Tunnel Toolkit',
    long_description=long_description,
    packages=found_packages,
    install_requires=install_reqs,
    entry_points={
        'console_scripts': [
            'iphttp = iptt.entrypoints:iphttp_run',
            'iphttpd = iptt.entrypoints:iphttpd_run',
        ]
    },
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    keywords=[
        'ipfs',
        'http'
    ]
)
