FROM nginx/unit:1.26.1-python3.10
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /welbex
COPY requirements.txt /welbex/
RUN apt update && apt install -y python3-pip                                  \
    && apt install -y cron                                                    \
    && pip3 install -r requirements.txt                                       \
    && apt remove -y python3-pip                                              \
    && apt autoremove --purge -y                                              \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list
COPY unit_config.json /docker-entrypoint.d/
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/docker-entrypoint.sh
COPY . /welbex/
RUN SECRET_KEY=empty python manage.py collectstatic --noinput
RUN (echo "*/3 * * * * cd /welbex && python ./manage.py relocate_cars") | crontab
EXPOSE 8000
