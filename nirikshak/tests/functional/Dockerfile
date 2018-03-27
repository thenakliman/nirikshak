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

CMD /home/functional_test.sh
