Preparation for start from scratch:

- `sudo mkdir /var/run/tuvermind`
- `sudo chown user:www-data /var/run/tuvermind`
- `sudo mkdir /tmp/tuvermind`
- `sudo chown user:www-data /tmp/tuvermind`
- `sudo mkdir /var/www/tuvermind`
- `sudo chown /var/www/tuvermind`
- `mkdir /var/www/tuvermind/static /var/www/tuvermind/media`
- `python3 manage.py migrate`
- `python3 manage.py collectstatic`

## Setup development environment with docker-compose
```shell
cd etc/dev.env
docker build -t tuvermind .

```
