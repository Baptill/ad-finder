# Rent Finder - Scraper Figaro Immobilier

## Description

Rent Finder est un scraper orienté objet pour récupérer automatiquement les données immobilières du site Figaro Immobilier. Il permet de surveiller les prix au m², les loyers et les délais de vente pour différentes villes.

## Architecture

Le projet suit une architecture similaire à `lbc-finder` avec une approche orientée objet :

```
rent-finder/
├── models/                 # Modèles de données
│   ├── location.py        # Classe Location
│   ├── scraping_parameters.py  # Paramètres de scraping
│   └── search.py          # Classe Search
├── scraper/               # Logique de scraping
│   ├── figaro_scraper.py  # Scraper principal
│   └── simple_extractor.py  # Extraction des données HTML
├── manager/               # Gestionnaire principal
│   └── rent_manager.py    # Gestionnaire des recherches
├── examples/              # Exemples d'utilisation
├── config.py              # Configuration
└── main.py               # Point d'entrée
```

## Installation

1. Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Configuration

Modifiez le fichier `config.py` pour ajouter vos recherches :

```python
from models import Search, Location, ScrapingParameters

# Créer une localisation
location = Location(
    country_id='FR',
    region_id='6',
    region_name='Normandie',
    department_id='50',
    department_name='Manche',
    city_label='Saint-Hilaire-du-Harcouët 50600',
    city='Saint-Hilaire-du-Harcouët',
    zipcode='50600',
    lat=48.58071,
    lng=-1.09334
)

# Créer une recherche
search = Search(
    name="Ma recherche",
    location=location,
    ville_id="50484",  # ID Figaro pour la ville
    delay=600,  # Délai entre les scrapings (secondes)
    handler=handle_data  # Fonction pour traiter les données
)

CONFIG = [search]
```

## Utilisation

### Lancement simple

```bash
python main.py
```

### Test du scraping

```bash
python examples/test_scraping.py
```

## Fonctionnalités

### Données récupérées

- Prix médian au m²
- Évolution des prix (1 an, 5 ans)
- Prix par nombre de pièces
- Loyers au m²
- Délais de vente

### Options de configuration

- Délai entre les requêtes
- Timeout des requêtes
- Nombre de tentatives
- Filtres par type de bien
- Headers HTTP personnalisables

## Exemple d'objet Location

```python
Location(
    country_id='FR',
    region_id='6',
    region_name='Bretagne',
    department_id='35',
    department_name='Ille-et-Vilaine',
    city_label='Saint-Malo 35400',
    city='Saint-Malo',
    zipcode='35400',
    lat=48.63974408001426,
    lng=-1.9846315221479245,
    source='city',
    provider='here',
    is_shape=True
)
```

## API

### RentManager

- `start()` : Démarre le gestionnaire
- `stop()` : Arrête le gestionnaire
- `force_scrape(search_name)` : Force un scraping immédiat

### Location

- `to_figaro_url_slug()` : Convertit en slug URL
- `to_figaro_url(ville_id)` : Génère l'URL complète

## Notes

- Le scraper respecte un délai entre les requêtes pour éviter la surcharge
- Le système gère les erreurs réseau et les tentatives de reconnexion
- Compatible avec toutes les villes disponibles sur Figaro Immobilier
