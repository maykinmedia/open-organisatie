.. _azure_entra_provision:

==============================================
Users en Groups provisionen via Azure Entra ID
==============================================

Om gebruikers en groepen automatisch naar je applicatie te synchroniseren, kan
Azure Entra ID gebruikt worden. Dit zorgt ervoor dat de juiste personen toegang
hebben tot de applicatie en dat groepslidmaatschappen consistent blijven.

.. _azure_entra_provision_steps:

Applicatie configureren voor provisioning
=========================================

1. Applicatie registreren in Azure Entra ID

    * Navigeer naar Azure Active Directory → Enterprise applications → New application
    * Kies Create your own application en geef een naam.
    * Klik op Create.

2. Provisioning credentials configureren

    * Navigeer naar de zojuist aangemaakte applicatie en ga naar "Provisioning" → "Connectivity".
    * Vul bij "Tenant URL" de SCIM 2.0 endpoint URL van je Open Organisatie installatie in, bijvoorbeeld:
      ``https://open-organisatie.<organization.local>/scim/v2/``
    * Vul bij "Secret Token" de API-token in die je hebt gegenereerd in Open Organisatie.
    * Test de verbinding om te verifiëren dat alles correct is ingesteld.
    * Klik op "Save" om de instellingen op te slaan.

3. Provisioning mappings instellen

    * Ga naar Mappings → Provision Azure Active Directory Users
    * Pas de gebruikers- en groepsattributen aan indien nodig.
    * Zorg ervoor dat de volgende minimale attributen worden gemapt:

    * User:

    .. image:: assets/user_mapping.png
        :width: 100%
        :alt: User mapping

    * Group:

    .. image:: assets/group_mapping.png
        :width: 100%
        :alt: Group mapping

4. Provisioning inschakelen

    * Navigeer terug naar het tabblad "Overview".
    * Klik op start provisioning.
    * Azure Entra ID begint nu met het synchroniseren van gebruikers en groepen naar je Open Organisatie installatie.

5. Controle en logging

    * Monitor de provisioning status en logs in de Azure portal om te controleren of de synchronisatie correct verloopt.
    * Je kunt testen door een testgebruiker of -groep aan te maken en te verifiëren dat deze correct in je applicatie verschijnt.

