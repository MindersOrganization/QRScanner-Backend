FROM python:3.10.11
ENV PYTHONUNBUFFERED 1
RUN mkdir /my_app_dir
WORKDIR /my_app_dir
ADD requirments.txt /my_app_dir/
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh
RUN pip install -r requirments.txt gunicorn
RUN apt-get update && apt-get install -y mariadb-client tzdata
RUN ln -fs /usr/share/zoneinfo/Africa/Cairo /etc/localtime && dpkg-reconfigure -f noninteractive tzdata
ADD . /my_app_dir/