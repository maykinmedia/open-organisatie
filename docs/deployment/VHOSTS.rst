Apache + mod-wsgi configuration
===============================

An example Apache2 vhost configuration follows::

    WSGIDaemonProcess openorganisatie-<target> threads=5 maximum-requests=1000 user=<user> group=staff
    WSGIRestrictStdout Off

    <VirtualHost *:80>
        ServerName my.domain.name

        ErrorLog "/srv/sites/openorganisatie/log/apache2/error.log"
        CustomLog "/srv/sites/openorganisatie/log/apache2/access.log" common

        WSGIProcessGroup openorganisatie-<target>

        Alias /media "/srv/sites/openorganisatie/media/"
        Alias /static "/srv/sites/openorganisatie/static/"

        WSGIScriptAlias / "/srv/sites/openorganisatie/src/openorganisatie/wsgi/wsgi_<target>.py"
    </VirtualHost>


Nginx + uwsgi + supervisor configuration
========================================

Supervisor/uwsgi:
-----------------

.. code::

    [program:uwsgi-openorganisatie-<target>]
    user = <user>
    command = /srv/sites/openorganisatie/env/bin/uwsgi --socket 127.0.0.1:8001 --wsgi-file /srv/sites/openorganisatie/src/openorganisatie/wsgi/wsgi_<target>.py
    home = /srv/sites/openorganisatie/env
    master = true
    processes = 8
    harakiri = 600
    autostart = true
    autorestart = true
    stderr_logfile = /srv/sites/openorganisatie/log/uwsgi_err.log
    stdout_logfile = /srv/sites/openorganisatie/log/uwsgi_out.log
    stopsignal = QUIT

Nginx
-----

.. code::

    upstream django_openorganisatie_<target> {
      ip_hash;
      server 127.0.0.1:8001;
    }

    server {
      listen :80;
      server_name  my.domain.name;

      access_log /srv/sites/openorganisatie/log/nginx-access.log;
      error_log /srv/sites/openorganisatie/log/nginx-error.log;

      location /500.html {
        root /srv/sites/openorganisatie/src/openorganisatie/templates/;
      }
      error_page 500 502 503 504 /500.html;

      location /static/ {
        alias /srv/sites/openorganisatie/static/;
        expires 30d;
      }

      location /media/ {
        alias /srv/sites/openorganisatie/media/;
        expires 30d;
      }

      location / {
        uwsgi_pass django_openorganisatie_<target>;
      }
    }
