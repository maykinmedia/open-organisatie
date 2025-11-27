.. _installation_observability_logging:

=======
Logging
=======

Logging is the practice of emitting log messages that describe what is happening in the
system, or "events" in short. Log events can have varying degrees of severity, such as
``debug``, ``info``, ``warning``, ``error`` or even ``critical``. By default, Open Organisatie
emits logs with level ``info`` and higher.

A collection of log events with a correlation ID (like a request or trace ID) allow one
to reconstruct the chain of events that took place which lead to a particular outcome.

Open Organisatie emits structured logs in JSON format (unless explicitly configured otherwise),
which should make log aggregation and analysis easier.

We try to keep a consistent log message structure, where the following keys
are (usually) present:

``source``
    The component in the application stack that produced the log entry. Typical
    values are ``uwsgi`` and ``app``.

``level``
    The severity level of the log message. One of ``debug``, ``info``, ``warning``,
    ``error`` or ``critical``.

``timestamp``
    The moment when the log entry was produced, a string in ISO-8601 format. Most of
    the logs have microsecond precision, but some of them are limited to second
    precision.

``event``
    The event that occurred, e.g. ``request_started`` or ``spawned worker (PID 123)``.
    This gives the semantic meaning to the log entry.

Other keys that frequently occur are:

``request_id``
    Present for application logs emitted during an HTTP request, makes it possible to
    correlate multiple log entries for a single request. Not available in logs emitted
    by background tasks or logs emitted before/after the Open Organisatie app.

.. tip:: Certain log aggregation solutions require you to configure "labels" to extract
   for efficient querying. You can use the above summary of log context keys to configure
   this according to your needs.

.. note:: We can not 100% guarantee that every log message will always be JSON due to
   limitations in third party software/packages that we use. Most (if not all) log
   aggregation technologies support handling both structured and unstructured logs.


.. _manual_logging:

Logging
=======

Format
------

Open Organisatie emits structured logs (using `structlog <https://www.structlog.org/en/stable/>`_).
A log line can be formatted like this:

.. code-block:: json

    {
        "id": 1,
        "naam": "test",
        "event": "medewerker_created",
        "user_id": null,
        "request_id": "2f9e9a5b-d549-4faa-a411-594aa8a52eee",
        "timestamp": "2025-05-19T14:09:20.339166Z",
        "logger": "openorganisatie.scim.api.viewsets.medewerker",
        "level": "info"
    }

Each log line will contain an ``event`` type, a ``timestamp`` and a ``level``.
Dependent on your configured ``LOG_LEVEL`` (see :ref:`installation_env_config` for more information),
only log lines with of that level or higher will be emitted.

Open Organisatie log events
---------------------------

Below is the list of logging ``event`` types that Open Organisatie can emit. In addition to the mentioned
context variables, these events will also have the **request bound metadata** described in the :ref:`django-structlog documentation <request_events>`.

API
~~~

* ``medewerker_created``: created a ``Medewerker`` via the API. Additional context: ``uuid``, ``naam``, ``medewerker_id``.
* ``medewerker_updated``: updated a ``Medewerker`` via the API. Additional context: ``uuid``, ``naam``, ``medewerker_id``.
* ``medewerker_deleted``: deleted a ``Medewerker`` via the API. Additional context: ``uuid``, ``naam``, ``medewerker_id``.

* ``team_created``: created a ``Team`` via the API. Additional context: ``uuid``, ``naam``.
* ``team_updated``: updated a ``Team`` via the API. Additional context: ``uuid``, ``naam``.
* ``team_deleted``: deleted a ``Team`` via the API. Additional context: ``uuid``, ``naam``.

* ``organisatorische_eenheid_created``: created a ``Organisatorische eenheid`` via the API. Additional context: ``uuid``, ``identificatie``, ``naam``.
* ``organisatorische_eenheid_updated``: updated a ``Organisatorische eenheid`` via the API. Additional context: ``uuid``, ``identificatie``, ``naam``.
* ``organisatorische_eenheid_deleted``: deleted a ``Organisatorische eenheid`` via the API. Additional context: ``uuid``, ``identificatie``, ``naam``.

* ``vestiging_created``: created a ``Vestiging`` via the API. Additional context: ``uuid``, ``vestigingsnummer``, ``naam``.
* ``vestiging_updated``: updated a ``Vestiging`` via the API. Additional context: ``uuid``, ``vestigingsnummer``, ``naam``.
* ``vestiging_deleted``: deleted a ``Vestiging`` via the API. Additional context: ``uuid``, ``vestigingsnummer``, ``naam``.

* ``functie_created``: created a ``Functie`` via the API. Additional context: ``uuid``, ``functie_omschrijving``.
* ``functie_updated``: updated a ``Functie`` via the API. Additional context: ``uuid``, ``functie_omschrijving``.
* ``functie_deleted``: deleted a ``Functie`` via the API. Additional context: ``uuid``, ``functie_omschrijving``.

* ``functietype_created``: created a ``FunctieType`` via the API. Additional context: ``uuid``, ``naam``.
* ``functietype_updated``: updated a ``FunctieType`` via the API. Additional context: ``uuid``, ``naam``.
* ``functietype_deleted``: deleted a ``FunctieType`` via the API. Additional context: ``uuid``, ``naam``.

SCIM
~~~~

* ``add_scim_user``: created a ``User`` via SCIM. Additional context: ``username``, ``first_name``, ``last_name``.
* ``update_scim_user``: updated a ``User`` via SCIM. Additional context: ``username``, ``operations``.

* ``scim_group_members_added``: created a ``Group`` via SCIM. Additional context: ``team``, ``team_id``, ``added_members``.
* ``scim_group_members_removed``: deleted a ``Group`` via SCIM. Additional context: ``team``, ``team_id``, ``removed_members``.


.. _manual_logging_exceptions:

Exceptions
----------

Handled exceptions follow a standardized JSON format to ensure consistency and improve error tracking.
Most fields are standard and include:
``title``, ``code``, ``status``, ``event``, ``source``, ``user_id``, ``request_id``, ``timestamp``, ``logger`` and ``level``.

A new field ``data`` has been added to provide detailed information about which input parameters caused the error in API calls.

.. code-block:: json

    {
        "title": "Authentication credentials were not provided.",
        "code": "not_authenticated",
        "status": 401,
        "data": {
            "detail": "Authentication credentials were not provided."
        },
        "event": "api.handled_exception",
        "user_id": null,
        "request_id": "68b46bf0-a5b8-43f7-a550-e37dee617bff",
        "source": "app",
        "timestamp": "2025-10-06T07:43:40.991929Z",
        "logger": "openorganisatie.utils.views",
        "level": "error"
    }

Uncaught exceptions that occur via the API are logged as ``api.uncaught_exception`` events
and contain the traceback of the exception.

.. code-block:: json

    {
        "event": "api.uncaught_exception",
        "request_id": "9a5c781d-b15c-4b3a-8910-e7968ae37cb6",
        "user_id": null,
        "timestamp": "2025-10-06T08:31:57.572352Z",
        "logger": "openorganisatie.utils.views",
        "level": "error",
        "exception": "Traceback (most recent call last):\n  File \"/usr/local/lib/python3.12/site-packages/rest_framework/views.py\", line 497, in dispatch\n    self.initial(request, *args, **kwargs)\n  File \"/usr/local/lib/python3.12/site-packages/vng_api_common/geo.py\", line 30, in initial\n    super().initial(request, *args, **kwargs)\n  File \"/usr/local/lib/python3.12/site-packages/rest_framework/views.py\", line 415, in initial\n    self.check_permissions(request)\n  File \"/usr/local/lib/python3.12/site-packages/rest_framework/views.py\", line 332, in check_permissions\n    if not permission.has_permission(request, self):\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/app/src/openorganisatie/utils/scim_middleware.py\", line 10, in has_permission\n    1 / 0\n    ~~^~~\nZeroDivisionError: division by zero"
    }

Third party library events
--------------------------

For more information about log events emitted by third party libraries, refer to the documentation
for that particular library

* :ref:`Django (via django-structlog) <request_events>`
* :ref:`Celery (via django-structlog) <request_events>`
