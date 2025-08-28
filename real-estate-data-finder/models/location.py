from dataclasses import dataclass
from typing import Optional


@dataclass
class Location:
    country_id: str
    region_id: str
    region_name: str
    department_id: str
    department_name: str
    city_label: str
    city: str
    zipcode: str
    lat: float
    lng: float
    source: str = "city"
    provider: str = "here"
    is_shape: bool = True

    def to_figaro_url_slug(self) -> str:
        city_slug = self.city.lower()
        city_slug = city_slug.replace("â", "a").replace("é", "e").replace("è", "e")
        city_slug = city_slug.replace("ê", "e").replace("ë", "e").replace("î", "i")
        city_slug = city_slug.replace("ï", "i").replace("ô", "o").replace("ö", "o")
        city_slug = city_slug.replace("û", "u").replace("ü", "u").replace("ù", "u")
        city_slug = city_slug.replace("ç", "c").replace("ñ", "n")
        city_slug = city_slug.replace(" ", "-").replace("'", "-")

        return city_slug

    def to_figaro_url(self, ville_id: Optional[str] = None) -> str:
        base_url = "https://immobilier.lefigaro.fr/prix-immobilier"
        city_slug = self.to_figaro_url_slug()

        if ville_id:
            return f"{base_url}/{city_slug}/ville-{ville_id}"
        else:
            return f"{base_url}/{city_slug}"
