Nirikshak can be installed using following steps on ubuntu 16.04

#. Installation of git using following command

.. code::

   # apt-get install git python-pip libyaml-dev libpython2.7-dev python3-distutils-extra python-apt libdbus-1-dev libdbus-glib-1-dev

#. Get the code of nirikshak from the git using following command

.. code::

  # git clone https://github.com/thenakliman/nirikshak

#. Install dependency for the nirikshak using pip

.. code::

  # pip install dbus-python tox

#. Install nirikshak using following command

.. code::

  # cd nirikshak
  # sudo python setup.py install
  # mkdir /etc/nirikshak
  # cp etc/nirikshak/nirikshak.conf /etc/nirikshak
  # mkdir /var/lib/nirikshak
