from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
import re


class SimpleDataExtractor:
    """Extracteur de données"""

    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, "html.parser")
        self.text = html_content

    def extract_all_data(self, type: str) -> Dict[str, Any]:
        """Extrait toutes les données de la page en utilisant des regex et sélecteurs simples"""
        if type == "appartment":
            data = {"appartement": self._extract_appartment_data()}
        else:
            data = {"maison": self._extract_house_data()}
        return data

    def _extract_appartment_data(self):
        data = {
            "prix_m2_median": self._extract_m2_sell_data("prix-m2-appartement"),
            "loyers_m2_median": self._extract_m2_rent_data("loyer-appartement"),
            "price_by_rooms": self._extract_sell_price_by_rooms(
                "Prix d'un appartement par nombre de pièces"
            ),
            "loyers_m2_by_rooms": self._extract_rent_price_by_rooms(
                "Loyer d'un appartement par nombre de pièces"
            ),
        }
        return data

    def _extract_house_data(self):
        data = {
            "prix_m2_median": self._extract_m2_sell_data("prix-m2-maison"),
            "price_m2_by_rooms": self._extract_m2_rent_data("loyer-maison"),
            "loyers_m2_median": self._extract_sell_price_by_rooms(
                "Prix d'une maison par nombre de pièces"
            ),
            "loyers_m2_by_rooms": self._extract_rent_price_by_rooms(
                "Loyer d'une maison par nombre de pièces"
            ),
        }
        return data

    def _extract_m2_sell_data(self, tag: str):
        price_data = {}
        sell_price = self.soup.find("h2", id=tag)
        if sell_price:
            strongs = sell_price.find_all_next("strong", limit=3)
            if len(strongs) == 3:
                price_data["prix_median_m2"] = self._convert_m2(
                    strongs[0].get_text(strip=True)
                )
                price_data["evolution_one_year"] = self._convert_evolution(
                    strongs[1].get_text(strip=True)
                )
                price_data["evolution_five_years"] = self._convert_evolution(
                    strongs[2].get_text(strip=True)
                )
        return price_data

    def _extract_m2_rent_data(self, tag: str):
        price_data = {}
        rent_price = self.soup.find("h2", id=tag)
        if rent_price:
            strongs = rent_price.find_all_next("strong", limit=3)
            if len(strongs) == 3:
                price_data["prix_rent_m2"] = self._convert_m2(
                    strongs[0].get_text(strip=True)
                )
                price_data["rent_evolution_one_year"] = self._convert_evolution(
                    strongs[1].get_text(strip=True)
                )
                price_data["rent_evolution_five_years"] = self._convert_evolution(
                    strongs[2].get_text(strip=True)
                )
        return price_data

    def _extract_sell_price_by_rooms(self, tag: str) -> Dict[str, int]:
        rooms_data = {}

        h3 = self.soup.find(
            "h3",
            string=lambda t: t and tag in t,
        )
        if not h3:
            return rooms_data

        table = h3.find_next("table")
        if not table:
            return rooms_data

        for row in table.select("tbody tr"):
            cols = row.find_all("td")
            if len(cols) >= 2:
                room_label = cols[0].get_text(strip=True)
                price_text = cols[1].get_text(strip=True)

                if "-" in price_text:
                    continue

                price_clean = price_text.split("€/m2")[0]
                price_num = int(re.sub(r"[^\d]", "", price_clean))
                rooms_data[room_label] = price_num
        return rooms_data

    def _extract_rent_price_by_rooms(self, tag: str) -> Dict[str, int]:
        rooms_data = {}

        h3 = self.soup.find(
            "h3",
            string=lambda t: t and tag in t,
        )
        if not h3:
            return rooms_data

        table = h3.find_next("table")
        if not table:
            return rooms_data

        for row in table.select("tbody tr"):
            cols = row.find_all("td")
            if len(cols) >= 2:
                room_label = cols[0].get_text(strip=True)
                price_text = cols[1].get_text(strip=True)

                if "-" in price_text:
                    continue

                price_clean = price_text.split("€/m2")[0]
                price_num = int(re.sub(r"[^\d]", "", price_clean))
                rooms_data[room_label] = price_num

        return rooms_data

    def _convert_evolution(self, evolution: str) -> int | None:
        """Convert string evolution in int evolution"""
        match = re.search(r"(-?\d+)\s*%", evolution)
        if match:
            return int(match.group(1))
        return None

    def _convert_m2(self, price_by_m2: str) -> int | None:
        """Convert string m2 price in int price"""
        match = re.search(r"([\d\s]+)\s*€/m2", price_by_m2)
        if match:
            return int(match.group(1).replace(" ", "").replace("\xa0", ""))
        return None
