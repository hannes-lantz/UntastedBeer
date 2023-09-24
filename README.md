# UntastedBeer
Script that should tell which beers available at sytembolaget from a given country that you have not yet untappd. (*Recommend to crate an alias for it instead*)

```bash
python3 systemet.py
```

## Limitations
Due to both systemet and untappd not having any open API the script only finds about 20 of the latest entries on bot sites. This is why the script saves all data it finds in a local csv file in order to remember more than your 20 lates beers from a given country. So the more often the script is run the better it will be at telling if a beer is tasted or not.

## Todo
* Get more data/info from the systemet response
* Maybe also save systemet data?
* Add more countries
* Put country data in a CSV file instead of hardcoded

## User example

Example input:
```python
Enter your Untappd username: *name*
Enter a country name: belgien
```

```python
Choose an option:
1. Print Systemet Beer Names
2. Print Untappd Beer Info
3. Print Not tasted Systemet Beers
4. Input Another Country
5. Exit
Enter your choice:
```

```python
Enter your choice: 3
==================================================
Unique Systemet Beers
==================================================
Beer 1: Gauloise
Beer 2: Stella Artois
Beer 3: Leffe
Beer 4: Lindemans Apple
Beer 5: Hoegaarden
Beer 6: Chimay blå
Beer 7: Omnipollo Levon
Beer 8: Timmermans
Beer 9: Stella Artois
Beer 10: De Koninck
Beer 11: St Pierre
Beer 12: Affligem Blond
Beer 13: Duvel
Beer 14: Jambe-de-Bois
Beer 15: Leffe
Beer 16: Tripel d Anvers
Beer 17: Timmermans
Beer 18: Bink Blond
Beer 19: Saison Dupont
Beer 20: Oude Quetsche
Beer 21: O.J. Blanche
Beer 22: Saison
Beer 23: Oude Mûre
Beer 24: St. Louis Körsbär
Beer 25: Swinkels Family Brewers
Beer 26: Rodenbach
Beer 27: 3 Fonteinen
Beer 28: Brouwerij De Ranke
Beer 29: Tripel Karmeliet
Beer 30: Kriek BOON
--------------------------------------------------
```
## Docker

To run the project in docker run

```bash
docker build -t systemet:latest .
```

to build the image and run

```bash
docker run -i -t systemet 
```

to run the program.