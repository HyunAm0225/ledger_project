FROM mysql:5.7

ENV MYSQL_ROOT_PASSWORD=mysql
ENV MYSQL_DATABASE=database

RUN echo "[mysqld]" > /etc/mysql/conf.d/charset.cnf \
    && echo "skip-character-set-client-handshake" >> /etc/mysql/conf.d/charset.cnf \
    && echo "character-set-server = utf8mb4" >> /etc/mysql/conf.d/charset.cnf \
    && echo "collation-server = utf8mb4_unicode_ci" >> /etc/mysql/conf.d/charset.cnf \
    && echo "init-connect = 'SET NAMES utf8mb4'" >> /etc/mysql/conf.d/charset.cnf \
    && echo "[client]" >> /etc/mysql/conf.d/charset.cnf \
    && echo "default-character-set = utf8mb4" >> /etc/mysql/conf.d/charset.cnf \
    && echo "[mysql]" >> /etc/mysql/conf.d/charset.cnf \
    && echo "default-character-set = utf8mb4" >> /etc/mysql/conf.d/charset.cnf \
    && echo "[mysqldump]" >> /etc/mysql/conf.d/charset.cnf \
    && echo "default-character-set = utf8mb4" >> /etc/mysql/conf.d/charset.cnf