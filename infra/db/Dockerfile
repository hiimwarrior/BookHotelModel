FROM mysql:8.0.34-oracle

ENV MYSQL_DATABASE=hotel_booking_db \
    MYSQL_USER=user \
    MYSQL_PASSWORD=password \
    MYSQL_ROOT_PASSWORD=rootpassword

COPY my.cnf /etc/mysql/conf.d/my.cnf

EXPOSE 3306
