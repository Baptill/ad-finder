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

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = ScrapingParameters()

    def get_url(self) -> str:
        return self.location.to_figaro_url(self.ville_id)
