FROM python:3
MAINTAINER Dzmitry Hlukhau 'dzmitry.hlukhau@outlook.com'

COPY . /app
WORKDIR /app
# pip freeze > ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ['python']
CMD [ "python", "./admin.py" ]
