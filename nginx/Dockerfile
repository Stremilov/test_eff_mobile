FROM nginx:1.21

# Удаление дефолтной конфигурации
RUN rm /etc/nginx/conf.d/default.conf

# Копирование конфигурации
COPY prod.conf /etc/nginx/conf.d/

# Создание директории для SSL-сертификатов
RUN mkdir -p /etc/nginx/ssl 