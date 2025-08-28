#!/usr/bin/env python3
"""
Script de debug pour analyser la structure HTML des pages Figaro Immobilier
"""

import sys
import os
import requests
import re

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Location, ScrapingParameters
from scraper import FigaroScraper


def debug_html_structure():
    """Capture et analyse la structure HTML d'une page Figaro"""
    print("=== Debug de la structure HTML ===")

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

    url = location.to_figaro_url("50484")
    print(f"URL: {url}")

    # Configuration du scraper
    parameters = ScrapingParameters(
        get_price_m2=True,
        get_price_evolution=True,
        get_rent_data=True,
        get_sale_delays=True,
        delay_between_requests=1.0,
        timeout=30,
    )

    scraper = FigaroScraper(parameters)

    try:
        response = scraper.session.get(url, timeout=parameters.timeout)
        response.raise_for_status()

        html_content = response.text

        # Sauvegarder le HTML pour analyse
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        print("✅ Page HTML sauvegardée dans debug_page.html")

        # Analyser les sections de loyer
        analyze_rent_sections(html_content)

    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        scraper.close()


def analyze_rent_sections(html_content: str):
    """Analyse les sections de loyer dans le HTML"""
    print("\n=== Analyse des sections de loyer ===")

    # Chercher toutes les occurrences de "loyer"
    loyer_matches = re.finditer(r"loyer", html_content, re.IGNORECASE)
    loyer_positions = []

    for match in loyer_matches:
        start = max(0, match.start() - 100)
        end = min(len(html_content), match.end() + 200)
        context = html_content[start:end]
        loyer_positions.append((match.start(), context))

    print(f"Nombre d'occurrences de 'loyer': {len(loyer_positions)}")

    # Afficher les contextes
    for i, (pos, context) in enumerate(loyer_positions[:10]):  # Limiter à 10
        print(f"\n--- Occurrence {i+1} (position {pos}) ---")
        print(context.replace("\n", " ").replace("\r", " "))

    # Chercher les prix avec contexte loyer
    print("\n=== Recherche de prix dans le contexte loyer ===")

    # Patterns pour les prix dans le contexte loyer
    price_patterns = [
        r"(\d[\d\s]*)\s*€/m2.*loyer",
        r"loyer.*(\d[\d\s]*)\s*€/m2",
        r"<strong[^>]*>(\d[\d\s]*)\s*€/m2</strong>.*loyer",
        r"loyer.*<strong[^>]*>(\d[\d\s]*)\s*€/m2</strong>",
    ]

    for pattern in price_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
        if matches:
            print(f"Pattern '{pattern}' trouvé: {matches}")

    # Chercher les évolutions
    print("\n=== Recherche d'évolutions ===")

    evolution_patterns = [
        r"([+-]?\d+)\s*%.*sur\s*1\s*an",
        r"([+-]?\d+)\s*%.*sur\s*5\s*ans",
        r"sur\s*1\s*an.*?([+-]?\d+)\s*%",
        r"sur\s*5\s*ans.*?([+-]?\d+)\s*%",
    ]

    for pattern in evolution_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        if matches:
            print(f"Pattern '{pattern}' trouvé: {matches}")

    # Chercher les sections spécifiques
    print("\n=== Recherche de sections spécifiques ===")

    # Chercher les sections avec "appartement" et "maison"
    sections = [
        ("appartement", r"appartement.*?(\d[\d\s]*)\s*€/m2"),
        ("maison", r"maison.*?(\d[\d\s]*)\s*€/m2"),
    ]

    for section_name, pattern in sections:
        matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
        if matches:
            print(f"Section '{section_name}' trouvée: {matches}")

    # Chercher les tableaux ou listes de prix
    print("\n=== Recherche de tableaux/listes ===")

    # Chercher les balises table, ul, ol qui pourraient contenir des prix
    table_patterns = [
        r"<table[^>]*>.*?(\d[\d\s]*)\s*€/m2.*?</table>",
        r"<ul[^>]*>.*?(\d[\d\s]*)\s*€/m2.*?</ul>",
        r"<ol[^>]*>.*?(\d[\d\s]*)\s*€/m2.*?</ol>",
    ]

    for pattern in table_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
        if matches:
            print(f"Tableau/liste trouvé: {matches}")


if __name__ == "__main__":
    debug_html_structure()


