.. _entiteit_koppeling:

==============================================
Koppeling tussen User en Medewerker
==============================================

Om gebruikers ``User`` automatisch te koppelen aan medewerkers uit de personeelsadministratie, 
wordt gebruikgemaakt van het attribuut dat is ingesteld in de configuratie: ``AttribuutMappingConfig``.

Via het veld ``medewerker_koppel_attribuut`` kan worden gekozen welk uniek attribuut wordt gebruikt om de relatie te leggen. 
Standaard is dit het personeelsnummer (``employee_number``), 
maar dit kan bijvoorbeeld ook het e-mailadres of een ander uniek attribuut zijn.

Wanneer een gebruiker wordt gesynchroniseerd vanuit Azure Entra ID, zal de applicatie dit attribuut gebruiken om een bijbehorende medewerker te zoeken. Wanneer een match wordt gevonden, 
worden gebruiker en medewerker aan elkaar gekoppeld.

Voorbeeld:
 - Azure User heeft `employeeNumber = "12345"`
 - Medewerker in het HR-systeem heeft `personeelsnummer = "12345"`
 - De koppeling wordt automatisch gelegd.

Zorg er dus voor dat in Azure Entra ID dezelfde waarde voorkomt in het gekozen attribuut zoals ingesteld in de applicatieconfiguratie.

Mogelijke attributen
--------------------

.. note::
    
    Let op dat het gekozen attribuut in beide systemen **uniek en identiek** moet zijn.

De beschikbare keuzes voor ``medewerker_koppel_attribuut`` zijn:

- ``employee_number`` — *Employee Number (Entra)*  
  Aanbevolen indien het personeelsnummer zowel in Azure Entra ID als in de medewerkersadministratie uniform is vastgelegd.

- ``email`` — *E-mailadres*  
  Geschikt wanneer het primaire e-mailadres uniek is voor iedere medewerker.

- ``username`` — *User principal name (UPN)*  
  Gebruik dit wanneer de UPN leidend is binnen de organisatie.

Wat gebeurt er bij geen match?
------------------------------
Als er op basis van het geselecteerde attribuut **geen medewerker wordt gevonden**, zijn er twee mogelijke situaties:

1. **De gebruiker is geen medewerker**  
   Bijvoorbeeld een gastaccount (extern).  
   In dat geval wordt **geen koppeling** gelegd en kan de gebruiker verder functioneren als externe gebruiker, afhankelijk van de ingestelde rechten en rollen.

2. **De gebruiker zou wél gekoppeld moeten zijn**  
   Dit kan voorkomen wanneer het attribuut ontbreekt of niet overeenkomt tussen Azure Entra ID en de medewerkersadministratie.  
   Controleer dan of het attribuut in beide systemen correct en identiek is ingevuld.

Wanneer de waarde later alsnog wordt bijgewerkt, zal de koppeling **automatisch** tot stand komen bij de volgende synchronisatie.
