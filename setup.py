from setuptools import find_packages, setup

setup(
    name='DotcoTools',
    packages=find_packages(include=['DotcoTools']),
    version='0.2.1',
    description='Functions for scraping and automating .co',
    author='f',
    install_requires=['selenium', 'beautifulsoup4', 'lxml', 'requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.1'],
    test_suite='tests'
)
