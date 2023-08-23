from setuptools import setup, find_packages

setup(
    name='ordinals-etl',
    author='Yujie Liu',
    description='Tools for exporting Bitcoin Ordinals to JSON',
    version='0.1.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests~=2.20',
        'python-dateutil~=2.7',
        'click~=7.0'
    ],
    entry_points={
        'console_scripts': [
            'ordinalsetl=ordinalsetl.cli:cli',
        ],
    },
)
