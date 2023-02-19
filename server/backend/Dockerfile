FROM ubuntu:20.04
ENV DEBIAN_FRONTEND="noninteractive"

LABEL maintainer="Mickey <boujeebit>" 

RUN apt-get update     && \
    apt-get upgrade -y && \
    apt-get install -y    \
      python3      \
      python3-pip  \
      libpq-dev    \
      apache2      \
      tmux         \
      nano         \
      openssl      \
      libsasl2-dev \
      python-dev   \
      libldap2-dev \
      libssl-dev   \
      libapache2-mod-wsgi-py3

RUN apt-get clean

ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY . /var/www/backend/

COPY certs/ /etc/apache2/ssl/

RUN chmod 664 /var/www/backend/db.sqlite3
RUN chown -R www-data:www-data /var/www/

COPY configs/prd/000-default.conf /etc/apache2/sites-available/000-default.conf
COPY configs/prd/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf

RUN a2enmod rewrite
RUN a2enmod ssl
RUN a2ensite default-ssl.conf

CMD apachectl -D FOREGROUND