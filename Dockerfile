FROM python:3.6

RUN apt-get update -y && apt-get install -yq make cmake gcc g++ unzip wget build-essential gcc zlib1g-dev

# Opencvのインストール
RUN ln -s /usr/include/libv4l1-videodev.h /usr/include/linux/videodev.h

RUN mkdir ~/tmp
RUN cd ~/tmp && wget https://github.com/Itseez/opencv/archive/3.1.0.zip && unzip 3.1.0.zip
RUN cd ~/tmp/opencv-3.1.0 && cmake CMakeLists.txt -DWITH_TBB=ON \
                                                  -DINSTALL_CREATE_DISTRIB=ON \
                                                  -DWITH_FFMPEG=OFF \
                                                  -DWITH_IPP=OFF \
                                                  -DCMAKE_INSTALL_PREFIX=/usr/local
RUN cd ~/tmp/opencv-3.1.0 && make -j2 && make install
 
# TensorflowとOpencvのインストール
RUN pip3 install numpy tensorflow opencv-python

ENV APP_NAME tensor-docker
WORKDIR /home/$APP_NAME

CMD [ '/bin/bash'  ]
