FROM ubuntu:16.04

RUN apt-get update -y && \
	apt-get -y install apt-utils wget git apache2 php \
                   mysql-client php-mysql libapache2-mod-php php-gd \
                   php-curl php-xmlrpc php-intl vim php-zip \
                   php-xml php-mbstring php-soap cron

RUN sed -i '/Windows Extensions/ a extension=mysql.so' /etc/php/7.0/apache2/php.ini && \
	sed -i '/Windows Extensions/ a extension=gd.so' /etc/php/7.0/apache2/php.ini  && \
		service apache2 restart

RUN rm -rf /var/www/html/*
RUN cd /var/www/html && ls -la && git clone -b MOODLE_32_STABLE  git://git.moodle.org/moodle.git .
RUN rm -rf /var/www/html/*.git
RUN mkdir -p /var/www/moodledata && chown -R www-data:www-data /var/www/*

RUN service apache2 restart
ADD scripts /root/scripts
ADD config.php /var/www/html/config.php
RUN chmod +x /root/scripts/*.sh
EXPOSE 80
EXPOSE 443
ENTRYPOINT ["/root/scripts/script.sh"]
