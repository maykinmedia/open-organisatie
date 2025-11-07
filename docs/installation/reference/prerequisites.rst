.. _installation_prerequisites:

Prerequisites
=============

While the `container images <https://hub.docker.com/r/maykinmedia/open-organisatie/>`_
contain all the necessary dependencies, Open Organisatie does require extra service to
deploy the full stack. These dependencies and their supported versions are
documented here.

The ``docker-compose.yml`` (not suitable for production usage!) in the root of the
repository also describes these dependencies.

PostgreSQL
----------

Open Organisatie currently only supports PostgreSQL as datastore.

The supported versions in the table below are tested in the CI pipeline.

================ =========== ======= ======= ======= =======
Postgres version 13 or lower 14      15      16      17
================ =========== ======= ======= ======= =======
Supported?       |cross|     |check| |check| |check| |check|
================ =========== ======= ======= ======= =======

.. warning:: Open Organisatie only supports maintained versions of PostgreSQL. Once a version is
   `EOL <https://www.postgresql.org/support/versioning/>`_, support will
   be dropped in the next release.

Redis
-----

Open Organisatie uses Redis as a cache backend and especially relevant for admin sessions.

Supported versions: 5, 6, 7.

.. |check| unicode:: U+2705 .. ✅
.. |cross| unicode:: U+274C .. ❌
