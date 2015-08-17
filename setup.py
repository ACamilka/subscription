try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from subscription import __version__

requirements = [
    'pika==0.9.14',
    'fake-factory==0.5.2'
]

setup(
    name='subscription',
    version=__version__,
    description='',
    author='Asanova Camilla',
    author_email='camalasan@yahoo.com',
    packages=[
        'subscription',
    ],
    package_dir={'subscription': 'subscription'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False
)