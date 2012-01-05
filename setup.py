import sys

try:
    from setuptools import setup
except ImportError:
    from distutils import setup

try:
    import distancematrix
    version = distancematrix.__version__
except ImportError:
    version = (0, 0, 1)

requirements = ['networkx','pymetis',]

if sys.version_info[0] < 3 and sys.version_info[1] < 7:
    requirements.append('importlib')

setup(
    name='distancematrix',
    version='.'.join(str(c) for c in version),
    author='Mike Axiak',
    author_email='mike@axiak.net',
    description='Optimally call distance matrix information for list of origin-dest pairs.',
    long_description=open("README.rst").read(),
    license='BSD',
    test_suite = 'tests.test_all',
    install_requires=requirements,
    url='http://github.com/axiak/pydistancematrix',
    packages=['distancematrix'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ])
