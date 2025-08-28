#!/usr/bin/env python3
"""
Exemple de test du scraping pour une ville spécifique
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Location, Search, ScrapingParameters
from manager import RentManager
import time


def simple_handler(data, search_name):
    """Handler simple pour afficher les données"""
    print(f"\n=== Test de scraping pour {search_name} ===")

    if "prix_global" in data:
        prix = data["prix_global"]
        print(f"Prix médian: {prix.get('prix_median_m2', 'N/A')} €/m²")

    if "ville" in data:
        ville = data["ville"]
        print(f"Ville: {ville.get('nom', 'N/A')}")

    print("Données récupérées avec succès!")


def test_single_scrape():
    """Test d'un scraping unique"""
    print("=== Test de scraping unique ===")

    # Configuration pour Saint-Hilaire-du-Harcouët
    location = Location(
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
    )

    search = Search(
        name="Test Saint-Hilaire",
        location=location,
        ville_id="50484",
        delay=60,  # 1 minute pour le test
        handler=simple_handler,
    )

    manager = RentManager([search])

    # Force un scraping immédiat
    success = manager.force_scrape(search.name)

    if success:
        print("✅ Test réussi!")
    else:
        print("❌ Test échoué!")


def test_url_generation():
    """Test de génération d'URL"""
    print("=== Test de génération d'URL ===")

    location = Location(
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
    )

    print(f"Slug de ville: {location.to_figaro_url_slug()}")
    print(f"URL sans ID: {location.to_figaro_url()}")
    print(f"URL avec ID: {location.to_figaro_url('50484')}")


if __name__ == "__main__":
    test_url_generation()
    print("\n" + "=" * 50)
    test_single_scrape()
