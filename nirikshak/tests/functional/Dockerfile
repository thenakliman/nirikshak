FROM ubuntu:latest
MAINTAINER thenakliman@gmail.com

# Update source repos
RUN apt-get update

# Install required Dev dependency
RUN apt-get install -y \
    git \
    python2.7 \
    python-pip \
    python-dev \
    libyaml-dev \
    libpython2.7-dev

# Create nirikshak sample conf file
RUN mkdir -p /etc/nirikshak /var/lib/nirikshak

# Clone the code
RUN git clone http://github.com/thenakliman/nirikshak

# Change work directory to the code
WORKDIR /nirikshak

# Copy test cases
COPY var/ /var/lib

# Copy nirikshak config file
COPY etc/ /etc

# Install nirikshak
RUN python setup.py install
