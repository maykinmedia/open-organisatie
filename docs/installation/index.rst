.. _installation_index:

============
Installation
============

This section briefly describes how the project is intended to be installed in
development, staging and production environments.

Before you begin
----------------

.. note:: These requirements are aimed towards public testing and production
   deployments, though they are _interesting_ to understand the workings of Open Organisatie.

* Ensure you have the :ref:`installation_prerequisites` available
* Make sure the target machine(s) have access to the Internet.
* The target machine(s) should be reachable via at least a local DNS entry:

  * Open Organisatie: ``open-organisatie.<organization.local>``
  * `Open Notificaties`_: ``open-notificaties.<organization.local>``

    .. note:: Notifications can be disabled using ``NOTIFICATIONS_DISABLED`` (see :ref:`installation_env_config`).


  The machine(s) do not need to be publicly accessible and do not need a public DNS
  entry. In some cases, you might want this but it's not recommended. The same machine
  can be used for both Open Organisatie and `Open Notificaties`_.

.. _`Open Notificaties`: https://github.com/open-zaak/open-notificaties


Guides
------

.. toctree::
   :maxdepth: 1

   docker_compose
   provision_superuser
   config/index
   updating

Reference
---------

.. toctree::
   :maxdepth: 1

   reference/prerequisites
   reference/cli
