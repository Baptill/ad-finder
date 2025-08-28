import requests
from bs4 import BeautifulSoup
from typing import Optional
import re


class URLFinder:
    """Utilitaire pour trouver l'ID de ville sur Figaro Immobilier"""

    @staticmethod
    def find_ville_id(city_name: str, zipcode: Optional[str] = None) -> Optional[str]:
        """
        Tente de trouver l'ID de ville sur Figaro Immobilier

        Args:
            city_name: Nom de la ville
            zipcode: Code postal (optionnel)

        Returns:
            L'ID de la ville si trouvé, None sinon
        """
        search_url = "https://immobilier.lefigaro.fr/prix-immobilier"

        try:
            # Normaliser le nom de ville pour l'URL
            city_slug = URLFinder._normalize_city_name(city_name)

            # Essayer avec le slug de base
            test_url = f"{search_url}/{city_slug}"
            response = requests.get(test_url, timeout=10)

            if response.status_code == 200:
                ville_id = URLFinder._extract_ville_id_from_page(response.text)
                if ville_id:
                    print(f"✅ ID trouvé pour {city_name}: {ville_id}")
                    print(f"   URL: {test_url}/ville-{ville_id}")
                    return ville_id

            # Si pas trouvé, essayer une recherche
            print(f"❌ URL directe non trouvée pour {city_name}")
            return URLFinder._search_via_figaro(city_name, zipcode)

        except Exception as e:
            print(f"❌ Erreur lors de la recherche pour {city_name}: {e}")
            return None

    @staticmethod
    def _normalize_city_name(city_name: str) -> str:
        """Normalise le nom de ville pour l'URL"""
        city_slug = city_name.lower()

        # Remplacer les caractères accentués
        replacements = {
            "â": "a",
            "à": "a",
            "á": "a",
            "ä": "a",
            "ê": "e",
            "è": "e",
            "é": "e",
            "ë": "e",
            "î": "i",
            "ì": "i",
            "í": "i",
            "ï": "i",
            "ô": "o",
            "ò": "o",
            "ó": "o",
            "ö": "o",
            "û": "u",
            "ù": "u",
            "ú": "u",
            "ü": "u",
            "ç": "c",
            "ñ": "n",
        }

        for accented, normal in replacements.items():
            city_slug = city_slug.replace(accented, normal)

        # Remplacer espaces et apostrophes par des tirets
        city_slug = city_slug.replace(" ", "-").replace("'", "-")
        city_slug = re.sub(r"-+", "-", city_slug)  # Éviter les doubles tirets

        return city_slug.strip("-")

    @staticmethod
    def _extract_ville_id_from_page(html_content: str) -> Optional[str]:
        """Extrait l'ID de ville depuis le contenu HTML"""
        soup = BeautifulSoup(html_content, "html.parser")

        # Chercher dans l'URL de la page ou les métadonnées
        # Pattern: ville-12345
        patterns = [
            r"ville-(\d+)",
            r"/ville-(\d+)",
            r'data-ville-id["\']?[=:]?\s*["\']?(\d+)',
            r'ville_id["\']?[=:]?\s*["\']?(\d+)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, html_content)
            if matches:
                return matches[0]

        return None

    @staticmethod
    def _search_via_figaro(
        city_name: str, zipcode: Optional[str] = None
    ) -> Optional[str]:
        """Recherche via le moteur de recherche Figaro"""
        # Cette méthode pourrait être améliorée pour utiliser l'API de recherche
        # ou simuler une recherche sur le site
        print(f"⚠️  Recherche manuelle requise pour {city_name}")
        if zipcode:
            print(f"   Code postal: {zipcode}")
        print(
            "   Veuillez chercher manuellement sur https://immobilier.lefigaro.fr/prix-immobilier"
        )
        return None

    @staticmethod
    def test_url(city_name: str, ville_id: str) -> bool:
        """
        Teste si une URL avec un ID de ville fonctionne

        Args:
            city_name: Nom de la ville
            ville_id: ID de la ville à tester

        Returns:
            True si l'URL fonctionne, False sinon
        """
        try:
            city_slug = URLFinder._normalize_city_name(city_name)
            test_url = f"https://immobilier.lefigaro.fr/prix-immobilier/{city_slug}/ville-{ville_id}"

            response = requests.get(test_url, timeout=10)

            if response.status_code == 200:
                # Vérifier que la page contient bien des données de prix
                if "prix médian" in response.text.lower() or "€/m2" in response.text:
                    print(f"✅ URL valide: {test_url}")
                    return True
                else:
                    print(f"⚠️  URL accessible mais sans données de prix: {test_url}")
                    return False
            else:
                print(
                    f"❌ URL non accessible (code {response.status_code}): {test_url}"
                )
                return False

        except Exception as e:
            print(f"❌ Erreur lors du test de l'URL: {e}")
            return False
