==============
Change history
==============

0.2.0 (23-01-2026)
==================

**New features**

* [:open-organisatie:`105`] Integrate `django-common` package and improve home page style
* [:open-api-framework:`176`] Implement mozilla-django-oidc-db
* [:open-api-framework:`152`] Introduce and config OTel (see :ref:`installation_observability_index`)

**Project maintance**

* Upgrade dependencies

    * django to 5.2.9
    * urllib3 to 2.6.3
    * commonground-api-common to 2.10.7
    * mozilla-django-oidc-db to 1.1.1

* [:open-organisatie:`101`] Add bump my version to release tools
* Updated `uwsgi logs` from event to msg for high-cardinality log messages.
* Fix `celery_beat` and `celery_worker` configuration issues.

**Documentation**

* [:open-api-framework:`197`] Fix documentation with maximum pagination `pageSize` in the OAS. 

0.1.0 (26-11-2025)
==================

🎉 First release of Open Organisatie.

For full project information, see the `documentation <https://open-organisatie.readthedocs.io/en/latest/>`_

Features:

* Organisatie API
* Identiteit API
