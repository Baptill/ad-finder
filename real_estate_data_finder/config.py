from models import Search, Location, ScrapingParameters
from typing import Dict, Any


# Exemple de configuration avec Saint-Hilaire-du-Harcouët
saint_hilaire_location = Location(
    country_id="FR",
    region_id="6",
    region_name="Normandie",
    department_id="50",
    department_name="Manche",
    city_label="Saint-Hilaire-du-Harcouët 50600",
    city="Saint-Hilaire-du-Harcouët",
    zipcode="50600",
    lat=48.58071,
    lng=-1.09334,
    source="city",
    provider="here",
    is_shape=True,
)

# Configuration personnalisée pour le scraping
custom_parameters = ScrapingParameters(
    get_price_m2=True,
    get_price_evolution=True,
    get_rent_data=True,
    get_sale_delays=True,
    delay_between_requests=2.0,  # 2 secondes entre les requêtes
    timeout=30,
)

CONFIG = [
    Search(
        name="Saint-Hilaire-du-Harcouët Prix Immobilier",
        location=saint_hilaire_location,
        ville_id="50484",  # ID spécifique pour Saint-Hilaire-du-Harcouët
        parameters=custom_parameters,
        delay=600,  # 10 minutes entre chaque scraping
        type="appartment",
    ),
]

# Exemple d'autres villes si besoin
"""
# Avranches
avranches_location = Location(
    country_id='FR',
    region_id='6',
    region_name='Normandie',
    department_id='50',
    department_name='Manche',
    city_label='Avranches 50300',
    city='Avranches',
    zipcode='50300',
    lat=48.6846,
    lng=-1.3572,
    source='city',
    provider='here',
    is_shape=True
)

CONFIG.append(
    Search(
        name="Avranches Prix Immobilier",
        location=avranches_location,
        ville_id="50025",  # ID à vérifier
        parameters=custom_parameters,
        delay=900,  # 15 minutes
        handler=handle_data
    )
)
"""
