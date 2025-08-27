import time
import threading
from typing import List, Union
from models import Search, ScrapingParameters
from scraper import FigaroScraper


class RentManager:
    """Gestionnaire principal pour le scraping des données immobilières"""

    def __init__(self, searches: Union[List[Search], Search]):
        self._searches: List[Search] = (
            searches if isinstance(searches, list) else [searches]
        )
        self._running = False

    def _scrape_search(self, search: Search) -> None:
        scraper = FigaroScraper(search.parameters or ScrapingParameters())

        try:
            while self._running:
                start_time = time.time()

                try:
                    print(f"Début du scraping pour '{search.name}'")
                    url = search.get_url()
                    data = scraper.scrape_url(url)

                    if data:
                        # Appeler le handler si défini
                        if search.handler:
                            search.handler(data, search.name)

                        print(f"Scraping réussi pour '{search.name}'")
                    else:
                        print(f"Aucune donnée récupérée pour '{search.name}'")

                except Exception as e:
                    print(f"Erreur lors du scraping de '{search.name}': {e}")

                # Calculer le temps d'attente
                elapsed = time.time() - start_time
                sleep_time = max(0, search.delay - elapsed)

                if sleep_time > 0 and self._running:
                    print(
                        f"Attente de {sleep_time:.1f}s avant le prochain scraping de '{search.name}'"
                    )
                    time.sleep(sleep_time)

        finally:
            scraper.close()

    def start(self) -> bool:
        if not self._searches:
            print(
                "Aucune recherche configurée. Veuillez créer des recherches dans config.py"
            )
            return False

        if self._running:
            print("Le gestionnaire est déjà en cours d'exécution")
            return False

        self._running = True
        print(f"Démarrage du gestionnaire avec {len(self._searches)} recherche(s)")

        for search in self._searches:
            thread = threading.Thread(
                target=self._scrape_search,
                args=(search,),
                name=f"RentFinder-{search.name}",
                daemon=True,
            )
            thread.start()
            print(f"Thread démarré pour '{search.name}'")

            time.sleep(2)

        return True

    def stop(self) -> None:
        if self._running:
            print("Arrêt du gestionnaire de scraping...")
            self._running = False
        else:
            print("Le gestionnaire n'est pas en cours d'exécution")

    def is_running(self) -> bool:
        return self._running

    def get_all_searches(self) -> List[str]:
        return [search.name for search in self._searches]

    def force_scrape(self, search_name: str) -> bool:
        search = next((s for s in self._searches if s.name == search_name), None)
        if not search:
            print(f"Recherche '{search_name}' introuvable")
            return False

        print(f"Force le scraping de '{search_name}'")
        scraper = FigaroScraper(search.parameters or ScrapingParameters())

        try:
            url = search.get_url()
            data = scraper.scrape_url(url)

            if data:
                if search.handler:
                    search.handler(data, search.name)
                print(f"Scraping forcé réussi pour '{search_name}'")
                return True
            else:
                print(
                    f"Aucune donnée récupérée lors du scraping forcé de '{search_name}'"
                )
                return False

        except Exception as e:
            print(f"Erreur lors du scraping forcé de '{search_name}': {e}")
            return False

        finally:
            scraper.close()
