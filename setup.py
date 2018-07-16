from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ethgoesbloom',
    version='0.0.1',
    description='Fills an Ethereum bloom filter',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kfichter/ethgoesbloom',
    author='Kelvin Fichter',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3'
    ],
    keywords='ethereum solidity contracts bloom filter',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'ethereum==2.3.0',
        'py-solc==3.1.0',
        'web3==4.4.1'
        'eth-bloom==1.0.0'
    ]
)
