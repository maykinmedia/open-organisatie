==================
openorganisatie
==================

:Version: 0.1.0
:Source: https://github.com/maykinmedia/openorganisatie
:Keywords: ``<keywords>``

|docs| |docker|

``<oneliner describing the project>``
(`Nederlandse versie`_)

Developed by `Maykin B.V.`_ for ``<client>``.


Introduction
============

``<describe the project in a few paragraphs and briefly mention the features>``


API specification
=================

|oas|

==============  ==============  =============================
Version         Release date    API specification
==============  ==============  =============================
latest          n/a             `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/openorganisatie/main/src/openorganisatie/api/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/openorganisatie/main/src/openorganisatie/api/openapi.yaml>`_,
                                (`diff <https://github.com/maykinmedia/openorganisatie/compare/0.1.0..main#diff-b9c28fec6c3f3fa5cff870d24601d6ab7027520f3b084cc767aefd258cb8c40a>`_)
0.1.0           YYYY-MM-DD      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/maykinmedia/openorganisatie/0.1.0/src/openorganisatie/api/openapi.yaml>`_,
                                `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/maykinmedia/openorganisatie/0.1.0/src/openorganisatie/api/openapi.yaml>`_
==============  ==============  =============================

Previous versions are supported for 6 month after the next version is released.

See: `All versions and changes <https://github.com/maykinmedia/openorganisatie/blob/main/CHANGELOG.rst>`_


Developers
==========

|build-status| |coverage| |ruff| |docker| |python-versions|

This repository contains the source code for openorganisatie. To quickly
get started, we recommend using the Docker image. You can also build the
project from the source code. For this, please look at 
`INSTALL.rst <INSTALL.rst>`_.

Quickstart
----------

1. Download and run openorganisatie:

   .. code:: bash

      wget https://raw.githubusercontent.com/maykinmedia/openorganisatie/main/docker-compose.yml
      docker-compose up -d --no-build
      docker-compose exec web src/manage.py loaddata demodata
      docker-compose exec web src/manage.py createsuperuser

2. In the browser, navigate to ``http://localhost:8000/`` to access the admin
   and the API.


References
==========

* `Documentation <https://openorganisatie.readthedocs.io/>`_
* `Docker image <https://hub.docker.com/r/maykinmedia/openorganisatie>`_
* `Issues <https://github.com/maykinmedia/openorganisatie/issues>`_
* `Code <https://github.com/maykinmedia/openorganisatie>`_
* `Community <https://TODO>`_


License
=======

Copyright © Maykin 2025

Licensed under the EUPL_


.. _`Nederlandse versie`: README.rst

.. _`Maykin B.V.`: https://www.maykinmedia.nl

.. _`EUPL`: LICENSE.md

.. |build-status| image:: https://github.com/maykinmedia/openorganisatie/actions/workflows/ci.yml/badge.svg?branch=main
    :alt: Build status
    :target: https://github.com/maykinmedia/openorganisatie/actions/workflows/ci.yml

.. |docs| image:: https://readthedocs.org/projects/openorganisatie/badge/?version=latest
    :target: https://openorganisatie.readthedocs.io/
    :alt: Documentation Status

.. |coverage| image:: https://codecov.io/github/maykinmedia/openorganisatie/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage
    :target: https://codecov.io/gh/maykinmedia/openorganisatie

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. |docker| image:: https://img.shields.io/docker/v/maykinmedia/openorganisatie?sort=semver
    :alt: Docker image
    :target: https://hub.docker.com/r/maykinmedia/openorganisatie

.. |python-versions| image:: https://img.shields.io/badge/python-3.12%2B-blue.svg
    :alt: Supported Python version

.. |oas| image:: https://github.com/maykinmedia/openorganisatie/actions/workflows/oas.yml/badge.svg
    :alt: OpenAPI specification checks
    :target: https://github.com/maykinmedia/openorganisatie/actions/workflows/oas.yml
