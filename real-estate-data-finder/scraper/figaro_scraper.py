import requests
import time
from typing import Dict, Any, Optional
from models import ScrapingParameters
from .simple_extractor import SimpleDataExtractor


class FigaroScraper:
    """Scraper principal pour le site Figaro Immobilier"""

    def __init__(self, parameters: ScrapingParameters):
        self.parameters = parameters
        self.session = requests.Session()
        self.session.headers.update(parameters.get_headers())

    def scrape_url(self, url: str, type: str) -> Optional[Dict[str, Any]]:
        for attempt in range(self.parameters.max_retries):
            try:
                if attempt > 0:
                    time.sleep(self.parameters.delay_between_requests * (attempt + 1))

                response = self.session.get(url, timeout=self.parameters.timeout)
                response.raise_for_status()
                extractor = SimpleDataExtractor(response.text)
                data = extractor.extract_all_data(type=type)

                data["metadata"] = {
                    "url": url,
                    "timestamp": time.time(),
                    "status_code": response.status_code,
                }
                return data

            except requests.exceptions.RequestException as e:
                print(
                    f"Erreur lors de la requête (tentative {attempt + 1}/{self.parameters.max_retries}): {e}"
                )
                if attempt == self.parameters.max_retries - 1:
                    print(
                        f"Échec du scraping après {self.parameters.max_retries} tentatives pour: {url}"
                    )
                    return None

            except Exception as e:
                print(f"Erreur inattendue lors du scraping: {e}")
                return None

        return None

    def close(self):
        """Ferme la session"""
        self.session.close()
