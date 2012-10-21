from setuptools import setup, find_packages


kwargs = {
    # Packages
    'packages': find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),
    'include_package_data': True,

    # Dependencies
    'install_requires': [
        'fabric>=1.4.3',
        'virtualenv>=1.8.2',
    ],

    'test_suite': 'tests',

    'scripts': ['bin/harvest'],

    # Metadata
    'name': 'harvest',
    'version': __import__('harvest').get_version(),
    'author': 'The Children\'s Hospital of Philadelphia',
    'author_email': 'cbmisupport@email.chop.edu',
    'description': 'Harvest project template',
    'license': 'BSD',
    'keywords': 'harvest metadata avocado serrano cilantro django',
    'url': 'http://cbmi.github.com/harvest/',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
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
