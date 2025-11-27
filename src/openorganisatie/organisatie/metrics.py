from opentelemetry import metrics

meter = metrics.get_meter("openorganisatie.organisatie")

medewerkers_create_counter = meter.create_counter(
    "openorganisatie.medewerker.creates",
    description="Amount of medewerkers created (via the API).",
    unit="1",
)
medewerkers_update_counter = meter.create_counter(
    "openorganisatie.medewerker.updates",
    description="Amount of medewerkers updated (via the API).",
    unit="1",
)
medewerkers_delete_counter = meter.create_counter(
    "openorganisatie.medewerker.deletes",
    description="Amount of medewerkers deleted (via the API).",
    unit="1",
)
