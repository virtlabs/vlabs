
# docker run -d --name DB -p 3306:3306 -v /DATA/moodle/mysql:/var/lib/mysql -e MYSQL_DATABASE=moodle -e MYSQL_ROOT_PASSWORD=moodle -e MYSQL_USER=moodle -e MYSQL_PASSWORD=moodle mysql
# docker run -d  -p 80:80 --env-file env.list -v /DATA/moodle/config.php:/var/www/html/config.php -v /DATA/moodle/data:/var/www/moodledata --link DB:DB moodlevlabs

