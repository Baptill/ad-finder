from models import Search, Location, ScrapingParameters
from typing import Dict, Any


def handle_data(data: Dict[str, Any], search_name: str) -> None:
    """Handler pour traiter les données récupérées"""
    print(f"\n=== Nouvelles données pour {search_name} ===")

    # Afficher les informations de la ville
    if "ville" in data and data["ville"]:
        ville = data["ville"]
        print(f"Ville: {ville.get('nom', 'N/A')} ({ville.get('code_postal', 'N/A')})")

    # Afficher les prix globaux
    if "prix_global" in data and data["prix_global"]:
        prix = data["prix_global"]
        print(f"\nPrix médian au m²: {prix.get('prix_median_m2', 'N/A')} €/m²")
        print(f"Évolution 1 an: {prix.get('evolution_1_an', 'N/A')}")
        print(f"Évolution 5 ans: {prix.get('evolution_5_ans', 'N/A')}")
        if "prix_bas_m2" in prix:
            print(f"Prix bas: {prix['prix_bas_m2']} €/m²")
        if "prix_haut_m2" in prix:
            print(f"Prix haut: {prix['prix_haut_m2']} €/m²")

    # Afficher les prix par pièces
    if "prix_par_pieces" in data and data["prix_par_pieces"]:
        print(f"\nPrix par nombre de pièces:")
        for pieces, prix in data["prix_par_pieces"].items():
            print(f"  {pieces}: {prix} €/m²")

    # Afficher les loyers
    if "loyers" in data and data["loyers"]:
        loyers = data["loyers"]
        if "loyer_median_m2" in loyers:
            print(f"\nLoyer médian: {loyers['loyer_median_m2']} €/m²")

    # Afficher les délais de vente
    if "delais_vente" in data and data["delais_vente"]:
        print(f"\nDélais de vente:")
        for pieces, delai in data["delais_vente"].items():
            print(f"  {pieces}: {delai} jours")

    print("=" * 50)


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
        handler=handle_data,
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
