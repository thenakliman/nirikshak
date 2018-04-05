# Copyright 2017 <thenakliman@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import setuptools


setuptools.setup(
    name='nirikshak',
    version='0.1a',
    description='Health Check tools for distributed system',
    author='thenakliman',
    author_email='thenakliman@gmail.com',
    packages=setuptools.find_packages(exclude=['nirikshak.tests']),
    install_requires=[
        "PyYAML==3.11",
        "psutil==5.2.2",
        "six==1.10.0",
        "ping",
        # Need to fix for following packages
        # "python-apt==1.1.0b1",
        # "python3-distutils-extra",
        # "python3-dbus",
        # "pkgutil",
        "requests==2.9.1"],
    entry_points={
        'console_scripts': [
            'nirikshak = nirikshak.cli.nk:main'
        ]
    }
)
