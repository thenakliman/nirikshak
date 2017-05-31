import setuptools


setuptools.setup(
    name='nirikshak',
    version='0.1a',
    description='Health Check',
    author='thenakliman',
    author_email='thenakliman@gmail.com',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'nirikshak = nirikshak.cli.nk:main'
        ]
    }
)
