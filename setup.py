from setuptools import setup, find_packages


setup(
    name='psu.oit.wdt.campusmap',
    description='PSU Campus Map',
    version='1.0.0.dev0',
    author='PSU - OIT - WDT',
    author_email='webteam@pdx.edu',
    maintainer='Wyatt Baldwin',
    maintainer_email='wbaldwin@pdx.edu',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=1.11',
        'django-arcutils>=2.18.0',
        'django-local-settings>=1.0b6',
        'django-pgcli>=0.0.2',
        'djangorestframework>=3.6.2',
        'Markdown>=2.6.8',
        'psycopg2>=2.7.1',
        'psu.oit.arc.tasks',
    ],
    extras_require={
        'dev': [
            'coverage',
            'flake8',
        ]
    }
)
