#Deriving the latest base image
# docker build -t aprojection:v1 ./
# docker run -p 5555:5555 -v /home/hlukhau/PycharmProjects/video/static:/app/static -v /home/hlukhau/PycharmProjects/video/files:/app/files aprojection:v1
# docker run -p 5555:5555 -v /home/hlukhau/PycharmProjects/video/static:/app/static -v /home/hlukhau/PycharmProjects/video/files:/app/files -v /run/user/1000/pulse/native:/run/user/1000/pulse/native ---device /dev/snd aprojection:v1
# docker tag aprojection:v1  hlukhau/aprojection:v1
# docker login -u hlukhau
# docker push hlukhau/aprojection:v1
FROM python:latest

#Labels as key value pair
MAINTAINER Dzmitry Hlukhau 'dzmitry.hlukhau@outlook.com'

# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /app

#to COPY the remote file at working directory in container
COPY . /app
# Now the structure looks like this '/usr/app/src/test.py'

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get install libasound2-dev
RUN pip install simpleaudio


RUN pip install --no-cache-dir -r requirements.txt

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.
CMD [ "python", "./admin.py"]