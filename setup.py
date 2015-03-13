from setuptools import setup, find_packages


setup(
    name='psu.campusmap',
    packages=find_packages(),
    install_requires=[
        'arcutils',
        'decorator',
        'django>=1.7.6',
        'djangorestframework>=3.1.0',
    ],
    extras_require={
        'dev': [
            'coverage',
            'invoke',
        ]
    }
)
