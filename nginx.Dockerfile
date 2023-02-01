FROM tuvermind as static

RUN python3 manage.py collectstatic --no-input

FROM tuvermind/spa as spa-ui

FROM nginx:1.23.3-alpine-slim

ENV TUVERMIND_SERVER_NAME="" \
    request_uri='$request_uri'

RUN mkdir -p /var/www/tuvermind/media/ && \
    chown -R nginx:nginx /var/www/tuvermind/media/

COPY --chown=nginx:nginx ./tuvermind.nginx /etc/nginx/conf.d/default.template
CMD envsubst < /etc/nginx/conf.d/default.template > /etc/nginx/conf.d/default.conf && \
    nginx -g 'daemon off;'

#USER nginx

COPY --from=static --chown=nginx:nginx /tmp/tuvermind/static /var/www/tuvermind/static
COPY --from=spa-ui --chown=nginx:nginx /build/ /var/www/tuvermind/spa/
COPY --chown=nginx:nginx key.pem /etc/nginx/ssl/key.pem
COPY --chown=nginx:nginx fullchain_pem.crt /etc/nginx/ssl/fullchain_pem.crt
COPY --chown=nginx:nginx ./src/public/images/favicon.png /var/www/tuvermind/favicon.png
COPY --chown=nginx:nginx ./src/media/ /var/www/tuvermind/media/
