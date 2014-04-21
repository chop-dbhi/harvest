import sys
from setuptools import setup, find_packages

install_requires = [
    'Fabric>=1.8',
    'virtualenv>=1.11',
]

if sys.version_info < (2, 7):
    install_requires.append('argparse>=1.2.1')
    install_requires.append('ordereddict>=1.1')


kwargs = {
    # Packages
    'packages': find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),
    'include_package_data': True,

    # Dependencies
    'install_requires': install_requires,

    'test_suite': 'test_suite',

    'scripts': ['bin/harvest'],

    # Metadata
    'name': 'harvest',
    'version': __import__('harvest').get_version(),
    'author': 'The Children\'s Hospital of Philadelphia',
    'author_email': 'cbmisupport@email.chop.edu',
    'description': 'Harvest Command Line Tool',
    'license': 'BSD',
    'keywords': 'harvest metadata avocado serrano cilantro django',
    'url': 'https://github.com/cbmi/harvest/',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
    ],
}

setup(**kwargs)
