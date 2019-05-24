# RailNL
De Conducteurs

Het programma maakt een lijnvoering door (een deel) van Nederland, deze lijnvoering bestaat uit een of meerdere trajecten. Het doel is om de Optimalisatie functie K zo hoog mogelijk te maken.
Wij hebben een aantal algoritmes gemaakt waarbij we die K zo hoog mogelijk proberen te krijgen. De K waarde hangt af van de totale reistijd, aantal bereden kritieke verbindingen en het aantal trajecten dat is gebruikt.

# De algoritmes:

- Random_trajecten

Bij dit algoritme worden er 10000 random trajecten gemaakt. Uit die 10000 trajecten wordt random een dienstregeling gemaakt en de k ervan berekent. Hierna wordt er weer random een dienstregeling gemaakt en wordt de k berekent en vergelijkt die k waarde met de vorige k waarde en onthoudt de dienstregeling met de hoogste k waardig. Dan maakt die weer een dienstregeling en kijkt die of die k waarde weer hoger is. Kortom hij onthoudt steeds de diensregeling met de hoogste k waarde en vergelijkt die weer met een nieuwe dienstregeling. Dit doet hij 1.000.000 keer. Alle 1.000.000 k waardes worden opgeslagen in een file en op laatst wordt, in dat file, het beste gevonde taject geprint met haar k waarde.

- Simulated_annealing

Simulated annealing neemt een bestaande oplossing als input en doet deze optimalizeren op basis van de optimalizatie functie K. Het aantal keer dat er aanpassingen gedaan worden hangt af van de input. Na elke aanpassing berekent het programma een K en als deze beter is dan wordt de aanpassing automatisch aangenomen. Echter als de aanpassing een verslechtering is hangt het van een kansfunctie af of deze wordt aangenomen. Deze kansfucntie is een functie van het aantal iteraties, gedaan en totaal, en de verslechtering. Als de boolean hillclimber == True bij de input wordt meegegeven zullen er geen  verslechtering worden aangenomen.

## Aan de slag (Getting Started)

### Vereisten (Prerequisites)

Deze codebase is volledig geschreven in [Python3.6.3](https://www.python.org/downloads/). In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

```
pip install -r requirements.txt
```

### Structuur

Alle Python scripts staan in de folder Code. In de map Data zitten alle input waardes en in de map resultaten worden alle resultaten opgeslagen door de code.

### Test

Om de code te draaien met de standaardconfiguratie (bv. brute-force en voorbeeld.csv) gebruik de instructie:

```
python main.py
```

## Auteurs

*   Gabe Otagho
*   Sander Nobel
*   Pjotr van Hulst


## Dankwoord

* StackOverflow
* Minor Programmeren at the UvA
* Daan van den Berg   
* Bas Terwijn
* Reitze Jansen
