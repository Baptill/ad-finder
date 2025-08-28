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

    manager = RentManager(searches=CONFIG)

    if manager.start():
        try:
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
