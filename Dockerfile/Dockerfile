FROM ubuntu:latest
MAINTAINER thenakliman@gmail.com

# Update source repos
RUN apt-get update

# Install required Dev dependency
RUN apt-get install -y \
    python2.7 \
    python-pip \
    git \
    tox \
    python-dev \
    python3-dev \
    libyaml-dev \
    libpython2.7-dev \
    python3-distutils-extra \
    python-apt \
    libdbus-1-dev \
    libdbus-glib-1-dev \
    vim

# Clone the code
RUN git clone http://github.com/thenakliman/nirikshak

# Install dependeny using pip
RUN pip install dbus-python tox

# Create nirikshak sample conf file
RUN mkdir -p /etc/nirikshak /var/lib/nirikshak

# Change work directory to the code
WORKDIR /nirikshak

# Copy test cases
COPY var/ /var/lib

# Copy nirikshak config file
COPY etc/ /etc/nirikshak

# Run the command for verification
CMD /bin/bash
