from setuptools import setup
from setuptools import find_packages


def reqs_parse(path):
    with open(path) as f:
        return f.read().splitlines()


install_reqs = reqs_parse('requirements.txt')
found_packages = find_packages(exclude=['tests', 'tests.*'])

setup(
    name='iptt',
    version='1.0.0',
    license='MIT',
    author='cipres',
    url='https://gitlab.com/galacteek/iptt/iptt',
    description='iptt',
    packages=found_packages,
    install_requires=install_reqs,
    entry_points={
        'console_scripts': [
            'iphttp = iptt.entrypoints:iphttp_run'
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
