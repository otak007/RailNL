# De algoritmes:

- Random_trajecten

Bij dit algoritme worden er 10000 random trajecten gemaakt. Uit die 10000 trajecten wordt random een dienstregeling gemaakt en de k ervan berekent. Hierna wordt er weer random een dienstregeling gemaakt en wordt de k berekent en vergelijkt die k waarde met de vorige k waarde en onthoudt de dienstregeling met de hoogste k waardig. Dan maakt die weer een dienstregeling en kijkt die of die k waarde weer hoger is. Kortom hij onthoudt steeds de diensregeling met de hoogste k waarde en vergelijkt die weer met een nieuwe dienstregeling. Dit doet hij 1.000.000 keer. Alle 1.000.000 k waardes worden opgeslagen in een file en op laatst wordt, in dat file, het beste gevonde taject geprint met haar k waarde.

- Greedy

Bij dit algoritme wordt voor elk station een traject gemaakt met dat station als begin. Bij het bepalen van het volgende station binnen dat traject kijkt hij steeds naar welke connectie de meeste punten oplevert en voegt deze toe aan het traject. Dit doet hij tot de maximale tijd bereikt is. Aan het einde van het traject worden alle overbodige connecties (connecties aan het eind die minpunten opleveren) van het traject afgehaald. Dan vergelijkt hij alle trajecten met elkaar en kiest hij het traject dat de meeste punten oplevert. 
