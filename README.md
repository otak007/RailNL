# RailNL
De Conducteurs

Het programma maakt een lijnvoering door (een deel) van Nederland, deze lijnvoering bestaat uit een of meerdere trajecten. Het doel is om de optimalisatie functie K zo hoog mogelijk te maken.
Wij hebben een aantal algoritmes gemaakt waarbij we die K zo hoog mogelijk proberen te krijgen. De K waarde hangt af van de totale reistijd, aantal bereden kritieke verbindingen en het aantal trajecten dat is gebruikt.

# Algoritmes

We hebben de volgende algoritmes gebruikt:

- Random
- Greedy
- Simulated annealing (met hill climber)
- Depth first

Deze zijn met uitleg te vinden in het mapje code -> algorithms

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
