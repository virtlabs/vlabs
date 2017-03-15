FROM ubuntu:16.04

RUN apt-get update -y && \
	apt-get -y install apt-utils wget git apache2 php \
                   mysql-client php-mysql libapache2-mod-php php-gd \
                   php-curl php-xmlrpc php-intl vim php-zip \
                   php-xml php-mbstring php-soap

RUN sed -i '/Windows Extensions/ a extension=mysql.so' /etc/php/7.0/apache2/php.ini && \
	sed -i '/Windows Extensions/ a extension=gd.so' /etc/php/7.0/apache2/php.ini  && \
		service apache2 restart

# RUN mkdir mud && cd mud && git clone git://git.moodle.org/moodle.git
# RUN cd /mud/moodle && git branch -a && git branch --track MOODLE_32_STABLE origin/MOODLE_32_STABLE && git checkout MOODLE_32_STABLE && cd ..
#RUN rm -f /var/www/index.html
#RUN cp -rf  /mud/moodle/* /var/www

#RUN cd /var/www/ && mkdir /var/www/moodledata  && chown -R www-data:www-data moodledata && \
#		chmod -R 755 ./ && chmod -R 755 moodledata 

# RUN sed -i 's|'/var/www/html'|/var/www/|g' /etc/apache2/sites-available/000-default.conf && \
#	sed -i 's|'/var/www/html'|/var/www/|g' /etc/apache2/sites-available/default-ssl.conf

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
