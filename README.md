# 概要
使い方とかの詳細は以下のリンクで
https://qiita.com/sey323/items/8cb10f90889a6d911cd4

# Docker
## ビルド
~~~
docker build -t docker-tensorflow:0.1 .
~~~

## Dockerの実行
~~~
docker run --rm -v `pwd`:/home/tensor-docker -it docker-tensorflow:0.1 /bin/bash
~~~
