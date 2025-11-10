## Notificaties
## Berichtkenmerken voor Open Organisatie API

Kanalen worden typisch per component gedefinieerd. Producers versturen berichten op bepaalde kanalen,
consumers ontvangen deze. Consumers abonneren zich via een notificatiecomponent (zoals <a href="https://notificaties-api.vng.cloud/api/v1/schema/" rel="nofollow">https://notificaties-api.vng.cloud/api/v1/schema/</a>) op berichten.

Hieronder staan de kanalen beschreven die door deze component gebruikt worden, met de kenmerken bij elk bericht.

De architectuur van de notificaties staat beschreven op <a href="https://github.com/VNG-Realisatie/notificaties-api" rel="nofollow">https://github.com/VNG-Realisatie/notificaties-api</a>.


### Medewerkers

**Kanaal**
`medewerkers`

**Main resource**

`medewerker`

**Kenmerken**

* `uuid`: Uniek identificerend nummer van de medewerker.
* `medewerker_id`: Interne identificatie van de medewerker (bijvoorbeeld voor acties of koppelingen).
* `voornaam`: Voornaam van de medewerker.
* `achternaam`: Achternaam van de medewerker.
* `emailadres`: E-mailadres van de medewerker.

**Resources en acties**

* <code>medewerker</code>: create, update, destroy


### users

**Kanaal**
`users`

**Main resource**

`user`

**Kenmerken**

* `scim_external_id`: Uniek identificerend nummer van de gebruiker in SCIM.
* `username`: Gebruikersnaam van de gebruiker.
* `email`: E-mailadres van de gebruiker.

**Resources en acties**

* <code>user</code>: create, update


