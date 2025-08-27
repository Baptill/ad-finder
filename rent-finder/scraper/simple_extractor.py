from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
import re


class SimpleDataExtractor:
    """Version simplifiée de l'extracteur de données pour éviter les problèmes de typage"""

    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, "html.parser")
        self.text = html_content

    def extract_all_data(self) -> Dict[str, Any]:
        """Extrait toutes les données de la page en utilisant des regex et sélecteurs simples"""
        data = {
            "prix_global": self._extract_price_data(),
            "prix_par_pieces": self._extract_price_by_rooms(),
            "loyers": self._extract_rent_data(),
            "delais_vente": self._extract_sale_delays(),
            "ville": self._extract_city_info(),
        }

        return data

    def _extract_price_data(self) -> Dict[str, Any]:
        """Extrait les données de prix principal"""
        price_data = {}

        # Prix médian - chercher dans le texte
        price_patterns = [
            r"(\d[\d\s]*)\s*€/m2.*prix\s*médian",
            r"prix\s*médian.*?(\d[\d\s]*)\s*€/m2",
            r"<strong[^>]*>(\d[\d\s]*)\s*€/m2</strong>.*médian",
            r"médian.*?<strong[^>]*>(\d[\d\s]*)\s*€/m2</strong>",
        ]

        for pattern in price_patterns:
            matches = re.findall(pattern, self.text, re.IGNORECASE | re.DOTALL)
            if matches:
                try:
                    price_data["prix_median_m2"] = int(matches[0].replace(" ", ""))
                    break
                except ValueError:
                    continue

        # Évolutions
        evolution_patterns = [
            (r"([+-]?\d+)\s*%.*sur\s*1\s*an", "evolution_1_an"),
            (r"([+-]?\d+)\s*%.*sur\s*5\s*ans", "evolution_5_ans"),
        ]

        for pattern, key in evolution_patterns:
            matches = re.findall(pattern, self.text, re.IGNORECASE)
            if matches:
                price_data[key] = f"{matches[0]}%"

        return price_data

    def _extract_price_by_rooms(self) -> Dict[str, int]:
        """Extrait les prix par nombre de pièces"""
        rooms_data = {}

        # Patterns pour les différents types de pièces
        room_patterns = [
            (r"Studios?\s*/\s*1\s*pièce.*?(\d[\d\s]*)\s*€/m2", "Studios / 1 pièce"),
            (r"2\s*pièces?.*?(\d[\d\s]*)\s*€/m2", "2 pièces"),
            (r"3\s*pièces?.*?(\d[\d\s]*)\s*€/m2", "3 pièces"),
            (r"4\s*pièces?.*?(\d[\d\s]*)\s*€/m2", "4 pièces"),
            (r"5\s*pièces?.*?(\d[\d\s]*)\s*€/m2", "5 pièces"),
            (r"6\s*pièces?.*?(\d[\d\s]*)\s*€/m2", "6 pièces"),
            (r"7\s*pièces?.*?(\d[\d\s]*)\s*€/m2", "7 pièces et plus"),
        ]

        for pattern, room_type in room_patterns:
            matches = re.findall(pattern, self.text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                try:
                    price = int(match.replace(" ", ""))
                    rooms_data[room_type] = price
                    break  # Premier match trouvé
                except ValueError:
                    continue

        return rooms_data

    def _extract_rent_data(self) -> Dict[str, Any]:
        """Extrait les données de loyer"""
        rent_data = {}

        # Chercher les sections loyer
        loyer_patterns = [
            r"Loyer.*?(\d[\d\s]*)\s*€/m2.*médian",
            r"loyer\s*médian.*?(\d[\d\s]*)\s*€/m2",
            r"<strong[^>]*>(\d[\d\s]*)\s*€/m2</strong>.*loyer",
        ]

        for pattern in loyer_patterns:
            matches = re.findall(pattern, self.text, re.IGNORECASE | re.DOTALL)
            if matches:
                try:
                    rent_data["loyer_median_m2"] = int(matches[0].replace(" ", ""))
                    break
                except ValueError:
                    continue

        return rent_data

    def _extract_sale_delays(self) -> Dict[str, int]:
        """Extrait les délais de vente"""
        delays_data = {}

        # Patterns pour les délais de vente
        delay_patterns = [
            (r"Studios?\s*/\s*1\s*pièce.*?(\d+)\s*j", "Studios / 1 pièce"),
            (r"2\s*pièces?.*?(\d+)\s*j", "2 pièces"),
            (r"3\s*pièces?.*?(\d+)\s*j", "3 pièces"),
            (r"4\s*pièces?.*?(\d+)\s*j", "4 pièces"),
            (r"5\s*pièces?.*?(\d+)\s*j", "5 pièces"),
        ]

        for pattern, room_type in delay_patterns:
            matches = re.findall(pattern, self.text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                try:
                    delays_data[room_type] = int(match)
                    break
                except ValueError:
                    continue

        return delays_data

    def _extract_city_info(self) -> Dict[str, str]:
        """Extrait les informations de la ville"""
        city_info = {}

        # Chercher dans le titre de la page
        title_patterns = [
            r"Prix\s+m2\s+immobilier\s+à\s+([^(]+)\s*\((\d+)\)",
            r"à\s+([^(]+)\s*\((\d+)\)",
        ]

        for pattern in title_patterns:
            matches = re.findall(pattern, self.text, re.IGNORECASE)
            if matches:
                city_info["nom"] = matches[0][0].strip()
                city_info["code_postal"] = matches[0][1]
                break

        return city_info
