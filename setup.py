from setuptools import setup

setup(
    name='secretkeeper',
    version='0.1.0',
    py_modules=['secretkeeper'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'secretkeeper = secretkeeper:cli',
        ],
    },
)