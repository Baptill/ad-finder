from manager import RentManager
from config import CONFIG
import signal
import sys


def signal_handler(sig, frame):
    print("\nArrêt du programme...")
    if "manager" in globals():
        manager.stop()
    sys.exit(0)


def main() -> None:
    global manager
    signal.signal(signal.SIGINT, signal_handler)

    print("=== Rent Finder - Scraper Figaro Immobilier ===")
    print(f"Nombre de recherches configurées: {len(CONFIG)}")

    manager = RentManager(searches=CONFIG)

    if manager.start():
        print("Gestionnaire démarré avec succès!")
        print("Appuyez sur Ctrl+C pour arrêter le programme")

        try:
            # Maintenir le programme en vie
            while manager.is_running():
                import time

                time.sleep(1)
        except KeyboardInterrupt:
            signal_handler(None, None)
    else:
        print("Erreur lors du démarrage du gestionnaire")
        sys.exit(1)


if __name__ == "__main__":
    main()
