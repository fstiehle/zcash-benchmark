FROM debian:jessie

RUN apt-get update && apt-get -qqy install --no-install-recommends \
    build-essential automake ncurses-dev libcurl4-openssl-dev libssl-dev \
    libgtest-dev make autoconf automake libtool git apt-utils pkg-config \
    libc6-dev libcurl3-dev libudev-dev m4 g++-multilib unzip git python \
    zlib1g-dev wget curl ca-certificates pwgen bsdmainutils

WORKDIR /root/
RUN git clone https://github.com/fstiehle/zcash-benchmark

WORKDIR /root/zcash-benchmark/zcash/
RUN git checkout benchmark

RUN ./zcutil/fetch-params.sh 
RUN ./zcutil/build.sh -j$(nproc)

WORKDIR /root/zcash-benchmark/benchmark-client/
RUN mkdir -p ~/.zcash && cp zcash.conf ~/.zcash/

WORKDIR /root/zcash-benchmark/zcash/src/
RUN ./zcashd