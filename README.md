## .env example
```ini
TUVERMIND_DEBUG=1

TUVERMIND_SECRET_KEY=DJANGO_SECRET_KEY
TUVERMIND_API_KEY=OPENWEATHER_API_KEY

TUVERMIND_REDIS_HOST=redis
TUVERMIND_REDIS_PORT=6379

TUVERMIND_DB_USER=django_user
TUVERMIND_DB_PASSWORD=django_user_password
TUVERMIND_DB_HOST=database
TUVERMIND_DB_PORT=5432

POSTGRES_PASSWORD=postgres_user_password

PGADMIN_DEFAULT_EMAIL=pgadmin@user.email
PGADMIN_DEFAULT_PASSWORD=pg_admin_password
```


## docker-compose deploy
```shell
# start your services
docker-compose up -d

# apply django migrations
docker-compose exec api python3 manage.py migrate
# collect project static files
docker-compose exec api python3 manage.py collectstatic --no-input
```
