#!/usr/bin/env python3
"""
Test de l'utilitaire de recherche d'ID de ville
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import URLFinder


def test_known_cities():
    """Test avec des villes connues"""
    print("=== Test de recherche d'ID pour des villes connues ===\n")

    known_cities = [
        ("Saint-Hilaire-du-Harcouët", "50600", "50484"),
        ("Avranches", "50300", None),  # ID à découvrir
        ("Saint-Malo", "35400", None),  # ID à découvrir
        ("Fougères", "35300", None),  # ID à découvrir
    ]

    for city, zipcode, expected_id in known_cities:
        print(f"🔍 Recherche pour {city} ({zipcode})")

        if expected_id:
            # Tester l'ID connu
            if URLFinder.test_url(city, expected_id):
                print(f"   ✅ ID confirmé: {expected_id}")
            else:
                print(f"   ❌ ID invalide: {expected_id}")
        else:
            # Chercher l'ID
            found_id = URLFinder.find_ville_id(city, zipcode)
            if found_id:
                print(f"   ✅ ID trouvé: {found_id}")
            else:
                print(f"   ❌ Aucun ID trouvé")

        print()


def test_url_generation():
    """Test de génération d'URL"""
    print("=== Test de génération d'URL ===\n")

    cities = [
        "Saint-Hilaire-du-Harcouët",
        "Saint-Malo",
        "Bourg-Saint-Maurice",
        "L'Île-d'Yeu",
    ]

    for city in cities:
        slug = URLFinder._normalize_city_name(city)
        print(f"{city} → {slug}")


if __name__ == "__main__":
    test_url_generation()
    print("\n" + "=" * 60 + "\n")
    test_known_cities()
