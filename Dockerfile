#Deriving the latest base image
# docker build -t aprojection:v1 ./
# docker run -p 5555:5555 -v /home/hlukhau/PycharmProjects/video/static:/app/static -v /home/hlukhau/PycharmProjects/video/files:/app/files aprojection:v1
# docker run -p 5555:5555 -v /home/hlukhau/PycharmProjects/video/static:/app/static -v /home/hlukhau/PycharmProjects/video/files:/app/files -v /run/user/1000/pulse/native:/run/user/1000/pulse/native ---device /dev/snd aprojection:v1
# docker tag aprojection:v1  hlukhau/aprojection:v1
# docker login -u hlukhau
# docker push hlukhau/aprojection:v1

#FROM python:latest
FROM python:3
MAINTAINER Dzmitry Hlukhau 'dzmitry.hlukhau@outlook.com'


RUN apt-get update -yy && \
    apt-get install -yy \
	alsa-utils \
	portaudio19-dev \
	python-all-dev

#RUN apt-get install -y libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev libsndfile1
#RUN apt-get install alsa-base pulseaudio \

WORKDIR /app

COPY . /app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./admin.py"]