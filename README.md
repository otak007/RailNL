# RailNL
De Conducteurs

Wij hebben een aantal algoritmes gemaakt waarbij we de K zo hoog mogelijk hebben gemaakt. De K waarde hangt af van de totale reistijd, aantal bereden kritieke verbindingen en het aantal trajecten dat is gebruikt.

# De algoritmes:

- Random_trajecten

Bij dit algoritme worden er 10000 random trajecten gemaakt. Uit die 10000 trajecten wordt random een dienstregeling gemaakt en de k ervan berekent. Hierna wordt er weer random een dienstregeling gemaakt en wordt de k berekent en vergelijkt die k waarde met de vorige k waarde en onthoudt de dienstregeling met de hoogste k waardig. Dan maakt die weer een dienstregeling en kijkt die of die k waarde weer hoger is. Kortom hij onthoudt steeds de diensregeling met de hoogste k waarde en vergelijkt die weer met een nieuwe dienstregeling. Dit doet hij 1.000.000 keer. Alle 1.000.000 k waardes worden opgeslagen in een file en op laatst wordt, in dat file, het beste gevonde taject geprint met haar k waarde.


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
