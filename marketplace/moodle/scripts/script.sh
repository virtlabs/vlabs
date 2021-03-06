#!/bin/bash

sed -i  -e "s/\$DB_HOST/$DB_HOST/g" -e "s/\$DB_NAME/$DB_NAME/g" -e "s/\$DB_USER/$DB_USER/g" -e "s/\$DB_PASSWD/$DB_PASSWD/g" -e "s|\$WWW_ROOT|$WWW_ROOT|g" /var/www/html/config.php

service cron start

crontab -u www-data /root/scripts/cronphp

service apache2 start

tail -f /var/log/apache2/error.log
