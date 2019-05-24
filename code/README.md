# De algoritmes:

- Random_trajecten

Bij dit algoritme worden er 10000 random trajecten gemaakt. Uit die 10000 trajecten wordt random een dienstregeling gemaakt en de k ervan berekent. Hierna wordt er weer random een dienstregeling gemaakt en wordt de k berekent en vergelijkt die k waarde met de vorige k waarde en onthoudt de dienstregeling met de hoogste k waardig. Dan maakt die weer een dienstregeling en kijkt die of die k waarde weer hoger is. Kortom hij onthoudt steeds de diensregeling met de hoogste k waarde en vergelijkt die weer met een nieuwe dienstregeling. Dit doet hij 1.000.000 keer. Alle 1.000.000 k waardes worden opgeslagen in een file en op laatst wordt, in dat file, het beste gevonde taject geprint met haar k waarde.
Als alle connecties kritiek zijn dan moet je in connections.py critical op 1 zetten en als niet alle connecties kritiek zijn dan moet je die op 0 zetten.

- Simulated_annealing

Simulated annealing neemt een bestaande oplossing als input en doet deze optimalizeren op basis van de optimalizatie functie K. Het aantal keer dat er aanpassingen gedaan worden hangt af van de input. Na elke aanpassing berekent het programma een K en als deze beter is dan wordt de aanpassing automatisch aangenomen. Echter als de aanpassing een verslechtering is hangt het van een kansfunctie af of deze wordt aangenomen. Deze kansfucntie is een functie van het aantal iteraties, gedaan en totaal, en de verslechtering. Als de boolean hillclimber == True bij de input wordt meegegeven zullen er geen  verslechtering worden aangenomen.
