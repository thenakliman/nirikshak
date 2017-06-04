import setuptools


setuptools.setup(
    name='nirikshak',
    version='0.1a',
<<<<<<< HEAD
    description='Health Check tools for distributed system',
    author='thenakliman',
    author_email='thenakliman@gmail.com',
    packages=setuptools.find_packages(),
    install_requires=[
        "PyYAML==3.11",
        "psutil==5.2.2",
        # Need to fix for following packages
        "python-apt==1.1.0b1",
        "python3-distutils-extra",
        "python3-dbus",
        "pkgutil",
        "requests==2.9.1"],
=======
    description='Health Check',
    author='thenakliman',
    author_email='thenakliman@gmail.com',
    packages=setuptools.find_packages(),
>>>>>>> 2217b24... Addition of setuptools for build and installation
    entry_points={
        'console_scripts': [
            'nirikshak = nirikshak.cli.nk:main'
        ]
    }
)
