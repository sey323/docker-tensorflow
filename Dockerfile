FROM ubuntu:16.04
MAINTAINER Seiichirou Nomura

RUN apt-get update -y && apt-get install -yq make cmake gcc g++ unzip wget build-essential gcc zlib1g-dev 

# Python3のインストール
WORKDIR /root/
RUN wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz \
        && tar zxf Python-3.6.0.tgz \
        && cd Python-3.6.0 \
        && ./configure \
        && make altinstall
ENV PYTHONIOENCODING "utf-8"
RUN apt-get install -y python3-pip python-qt4

# Opencvのインストール
RUN apt-get -y install build-essential pkg-config libjpeg-dev libpng12-dev libtiff5-dev libopenexr-dev libavcodec-dev libavformat-dev yasm libfaac-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev libswscale-dev libjasper-dev libdc1394-22-dev libv4l-dev libgstreamer1.0-dev libgstreamer-plugins-base0.10-dev libgstreamer-plugins-base1.0-dev libtbb2 libtbb-dev libeigen3-dev
RUN ln -s /usr/include/libv4l1-videodev.h /usr/include/linux/videodev.h
 
RUN mkdir ~/tmp
RUN cd ~/tmp && wget https://github.com/Itseez/opencv/archive/3.1.0.zip && unzip 3.1.0.zip
RUN cd ~/tmp/opencv-3.1.0 && cmake CMakeLists.txt -DWITH_TBB=ON -DINSTALL_CREATE_DISTRIB=ON -DWITH_FFMPEG=OFF -DCMAKE_INSTALL_PREFIX=/usr/local
RUN cd ~/tmp/opencv-3.1.0 && make -j2 && make install

# TensorflowとOpencvのインストール
RUN pip3 install numpy tensorflow opencv-python

ENV APP_NAME tensor-docker
WORKDIR /home/$APP_NAME

CMD [ '/bin/bash'  ]
