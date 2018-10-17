FROM debian:stretch

MAINTAINER Adam Cecile <acecile@le-vert.net>

ENV TERM xterm
ENV HOSTNAME cuda-xmr-stak.local
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /root

# Upgrade base system and install wget to download GPG key
RUN apt update \
    && apt -y -o 'Dpkg::Options::=--force-confdef' -o 'Dpkg::Options::=--force-confold' dist-upgrade \
    && apt-get -y -o 'Dpkg::Options::=--force-confdef' -o 'Dpkg::Options::=--force-confold' --no-install-recommends install wget ca-certificates gnupg python3 \
    && rm -rf /var/lib/apt/lists/*

# Install my custom repository with mining Debian packages
# and then install xmr-stak (without CUDA dependency, this will be handled by nvidia-docker)
# Need procps because xmr-stak will try to raise large page memory value
COPY fake-cuda-deps-for-nvidia-docker_1.0_all.deb /tmp/
COPY gen-nvidida-txt.py /usr/local/bin/
RUN wget -O - https://packages.le-vert.net/packages.le-vert.net.gpg.key | apt-key add - \
    && echo "deb http://packages.le-vert.net/mining/debian stretch cuda9" > /etc/apt/sources.list.d/packages_le_vert_net_mining.list \
    && echo "deb http://deb.debian.org/debian stretch contrib non-free" >> /etc/apt/sources.list \
    && apt update \
    && dpkg -i /tmp/fake-cuda-deps-for-nvidia-docker_1.0_all.deb && rm -f /tmp/fake-cuda-deps-for-nvidia-docker_1.0_all.deb \
    && apt-get -y -o 'Dpkg::Options::=--force-confdef' -o 'Dpkg::Options::=--force-confold' --no-install-recommends --ignore-missing install procps xmr-stak xmr-stak-cuda \
    && rm -rf /var/lib/apt/lists/*

# nvidia-container-runtime @ https://gitlab.com/nvidia/cuda/blob/ubuntu16.04/8.0/runtime/Dockerfile
ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64
LABEL com.nvidia.volumes.needed="nvidia_driver"
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
