FROM python:3.10.11
ENV PYTHONUNBUFFERED 1
RUN mkdir /my_app_dir
WORKDIR /my_app_dir
ADD requirements.txt /my_app_dir/
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh
RUN pip install -r requirements.txt gunicorn
RUN apt-get update && apt-get install -y mariadb-client
ADD . /my_app_dir/