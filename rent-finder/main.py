from scraper import FigaroScraper
from models import ScrapingParameters
from config import CONFIG
import json


def main() -> None:
    if not CONFIG:
        print(
            "Aucune recherche configurée. Veuillez créer des recherches dans config.py"
        )
        return

    search = CONFIG[0]
    scraper = FigaroScraper(search.parameters or ScrapingParameters())

    try:
        url = search.get_url()
        data = scraper.scrape_url(url, search.type)
        if data:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("Aucune donnée récupérée")

    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        scraper.close()

    print("Scraping terminé.")


if __name__ == "__main__":
    main()
