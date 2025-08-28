from dataclasses import dataclass
from typing import Callable, Optional, Dict, Any
from .location import Location
from .scraping_parameters import ScrapingParameters


@dataclass
class Search:
    name: str
    location: Location
    ville_id: Optional[str] = None
    parameters: Optional[ScrapingParameters] = None
    delay: float = 300.0  # 5 minutes par défaut
    handler: Optional[Callable[[Dict[str, Any], str], None]] = None
    type: str = "appartment"

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = ScrapingParameters()

    def get_url(self) -> str:
        """Format l'URL avec les informations de la ville

        Returns:
            str: url de la ville
        """
        return self.location.to_figaro_url(self.ville_id)
