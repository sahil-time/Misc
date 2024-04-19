# Use the latest LTS version of Ubuntu as the base image
FROM ubuntu:latest

# Install a few packages
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get install -y cmake
RUN apt-get install -y python3-pip
RUN apt-get install -y software-properties-common

# Install Conan using pip3, specifically the 1.60.0 version for Google Orbit
RUN pip3 uninstall conan
RUN pip3 install "conan==1.60.0"

# Install Google Orbit Repo
RUN git clone https://github.com/google/orbit.git

# Copy the required patch and the library
COPY docker_patch.diff /orbit
# COPY zlib-1.2.13.tar.gz /orbit

# Patch the diff
WORKDIR /orbit
RUN git apply --reject --whitespace=fix docker_patch.diff
RUN git add .

# Delete stale lists
CMD rm -rf /var/lib/apt/lists/*

# Delete stale lists and exec bash shell
CMD rm -rf /var/lib/apt/lists/*; /bin/bash
